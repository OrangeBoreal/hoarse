# Standard Library
from collections import OrderedDict
from itertools import groupby

# Hoarse
from hoarse.models.competitors import Group, Entry
from hoarse.models.exceptions import NoMoreRuns


class Competition(object):
    """
    A competition contains :
        - a list of competitors partitioned in groups
        - a competition style
        - an ensemble of runs associated to each competitors
    """
    def __init__(self):
        self.tests = []
        self.groups = []

        # competitorsGroups is a sorted list of tuples of competitors and
        # their group
        self.competitorsGroups = []

    @property
    def competitors(self):
        return [competitor for competitor, __ in self.competitorsGroups]

    def addTest(self, styleSettings):
        test = CompetitionTest(
            competition=self, styleSettings=styleSettings
        )
        self.tests.append(test)
        return test

    def getGroup(self, groupId, create=False):
        """
        Gets a group b id in the existing groups.
        Can create it if necessary, if create is set to True.
        """
        for group in self.groups:
            if group.id == groupId:
                return group

        if create:
            group = Group(id=groupId)
            self.groups.append(group)
            return group

        else:
            raise ValueError("Group {} not found".format(groupId))

    def computeGroups(self, competitorsGroupIds):
        """
        Transforms ids into real groups
        """
        # Note : when getGroup creates a group, it's added to self.groups
        self.competitorsGroups = [
            (competitor, self.getGroup(groupId, create=True))
            for competitor, groupId in competitorsGroupIds
        ]


class CompetitionTest(object):
    """
    Test here means Trial, not UnitTest.
    """
    def __init__(self, competition, styleSettings):
        """
        At this point, groups are created, but empty.
        """
        self.competition = competition
        # Hungarian, korean, ...
        self.styleSettings = styleSettings
        # The tedious details of the aforementioned style
        self.runSettings = list(styleSettings.createRunSettings())
        # The number of runs in the style (eg hungarian: 9, korean: 6)
        self.totalRunNumber = len(self.runSettings)

        # This is the moment when competitors enter the test for good.
        for competitor, group in competition.competitorsGroups:
            group.entries.append(
                Entry.enterTest(
                    competitor=competitor, group=group, test=self
                )
            )

    @property
    def groups(self):
        return self.competition.groups

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
        for competitor, runs in groupby(self.runs, key=lambda run: run.competitor):
            competitorList.append(competitor)
            if doSum:
                total = 0
                target = 0
                for run in runs:
                    total += run.score()
                    target += run.targetScore()
                scoreList.append((total, target))
            else:
                scoreList.append([(run.score(), run.targetScore()) for run in runs])
        return dict(zip(competitorList, scoreList))

    def getFirstUncompletedRun(self):
        return next(iter(run for run in self.runs if not run.completed))

    @property
    def competitors(self):
        return self.competition.competitors

    @property
    def runs(self):
        for group in self.groups:
            for run in group.runs:
                yield run

    def getNextRun(self, currentRun, next_by="competitors", direction=1):
        """
        currentRun is a run object
        next_by can be "competitors" or "runs" or "group"
        direction can be 1 or -1
        Return a run that's "next" to the currentRun (before or after)
        """
        runNumber, competitor = currentRun.runNumber, currentRun.competitor

        # When we click left or right
        if next_by == "competitors":
            # We make the whole list of all runs in "natural" order
            list_to_use = list(self.runs)

        elif next_by == "runs":
            # We just take the list of this competitor's runs
            list_to_use = currentRun.entry.runs

        # we find the current run in the list
        index = list_to_use.index(currentRun)
        index = index + direction
        if index < 0:
            index = 0

        try:
            # we find the new run in the list
            return list_to_use[index]
        except IndexError:
            # when we overflow while changing runs for a
            # given competitor, we don't want to go to the results page.
            if next_by == "runs":
                return currentRun

            else:
                raise NoMoreRuns
