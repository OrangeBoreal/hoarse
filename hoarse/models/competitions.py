from hoarse.models.runs import Run
from collections import OrderedDict
from itertools import groupby

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
        self.styleSettings = styleSettings
        self.runSettings = list(styleSettings.createRunSettings())

        self.totalRunNumber = len(self.runSettings)

        self.runs = OrderedDict()
        for runNumber, runSettings in enumerate(self.runSettings):
            for competitor in self.competitors:
                self.runs[(runNumber, competitor)] = Run(
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
        aggregate = sum if doSum else list

        return {
            competitor: aggregate(run.score() for run in runs)
            for competitor, runs in groupby(self.runsByCompetitors(), key=lambda x: x.competitor)
        }

    def runsByCompetitors(self):
        """
        Returns runs ordered by competitors
        """
        return sorted(self.runs.values(), key=lambda x: (x.competitor.id, x.runNumber))

    def getFirstUncompletedRun(self):
        return next(iter(run for run in self.runs.values() if not run.completed))

    def getNextRun(self, currentRun, by="competitors", direction=1):
        """
        Return a run that's "next" to the currentRun
        by can be "competitors" or "runs"
        direction can be 1 or -1
        """
        runNumber, competitor = currentRun.runNumber, currentRun.competitor
        if by == "runs":
            if 0 <= runNumber + direction < self.totalRunNumber:
                runNumber += direction
        elif by == "competitors":
            index = self.competitors.index(competitor)
            if index + direction < 0:
                competitor = self.competitors[-1]
                runNumber = max(0, runNumber - 1)
            elif index + direction >= len(self.competitors):
                competitor = self.competitors[0]
                if runNumber >= self.totalRunNumber -1:
                    raise self.NoMoreRuns
                runNumber += 1
            else:
                competitor = self.competitors[index + direction]
        return self.runs[(runNumber, competitor)]

    @property
    def competitors(self):
        return self.competition.competitors
