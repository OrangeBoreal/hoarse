# Standard Library
from collections import OrderedDict
from itertools import groupby

# Hoarse
from hoarse.models.runs import Run


class Competition(object):
    """
    A competition contains :
        - a list of competitors partitioned in groups
        - a competition style
        - an ensemble of runs associated to each competitors
    """
    def __init__(self):
        self.tests = []
        self.competitors = []

    def addTest(self, styleSettings):
        test = CompetitionTest(competition=self, styleSettings=styleSettings)
        self.tests.append(test)
        return test


class CompetitionTest(object):
    """
    Test here means Trial, not UnitTest.
    """
    def __init__(self, competition, styleSettings):
        self.competition = competition
        #hungarian, korean, ...
        self.styleSettings = styleSettings
        #the tedious details of the aforementioned style
        self.runSettings = list(styleSettings.createRunSettings())
        #the number of runs in the style (eg hungarian: 9, korean: 6)
        self.totalRunNumber = len(self.runSettings)
        #the list of groups for this test
        self.groups = []
        for competitor in self.competitors:
            if competitor.group not in self.groups:
                self.groups.append(competitor.group)        

        #is it initialized before or after group are set?
        #seems to be initialized just before the first run setting
        #how about if we change the groups afterwards?
        self.runs = OrderedDict()
        for group in self.groups:
            for runNumber, runSettings in enumerate(self.runSettings):
                for competitor in self.competitors:
                    self.runs[(group, runNumber, competitor)] = Run(
                        runNumber=runNumber,
                        runSettings=runSettings,
                        competitor=competitor,
                    )

    class NoMoreRuns(Exception):
        pass

    def getScoresPerCompetitor(self, doSum=False):
        """
        Returns a dict like:
        {
            competitor_1: [run_1_score, run_2_score, ...],
            ...
        }
        """
        competitorList = []
        scoreList = []
        
        for competitor, runs in groupby(self.runsByCompetitors(), key=lambda x: x.competitor):
            competitorList.append(competitor)
            if doSum:
                total = 0
                target = 0
                for run in runs:      
                    total += run.score() 
                    target += run.targetScore()
                scoreList.append((total,target))
            else:
                scoreList.append([(run.score(), run.targetScore()) for run in runs])
        return dict(zip(competitorList, scoreList))
    

    def runsByCompetitors(self):
        """
        Returns runs ordered by competitors
        """
        return sorted(self.runs.values(), key=lambda x: (x.competitor.id, x.runNumber))

    def getFirstUncompletedRun(self):
        return next(iter(run for run in self.runs.values() if not run.completed))

    def getNextRun(self, currentRun, next_by="competitors", direction=1):
        """
        Return a run that's "next" to the currentRun
        next_by can be "competitors" or "runs"
        direction can be 1 or -1
        """
        runNumber, competitor = currentRun.runNumber, currentRun.competitor
        group = competitor.group
        print(group)
        if next_by == "runs":
            if 0 <= runNumber + direction < self.totalRunNumber:
                runNumber += direction
        elif next_by == "competitors":
            keys = list(self.runs.keys())  # Already sorted because it comes from an OrderedDict
            print(keys)
            index = keys.index((group, runNumber, competitor))            
            new_index = index + direction
            if 0 <= new_index < len(keys):
                group, runNumber, competitor = keys[new_index]
            elif new_index > self.totalRunNumber:
                raise self.NoMoreRuns()

        return self.runs[(group, runNumber, competitor)]

    @property
    def competitors(self):
        return self.competition.competitors
