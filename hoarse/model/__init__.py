from enum import Enum
import re
from collections import defaultdict


class Competitor(object):
    """
    Define the attributes of a competitor
    """
    def __init__(self, riderName, i, horseName='', groupNumber=-1, idxInGroup = -1):
        self.riderName = riderName
        self.horseName = horseName
        self.id = i
        self.groupNumber = groupNumber
        self.idxInGroup = idxInGroup


# class CompetitionStyle(Enum):
#     """
#     Enumeration of pre-implemented competition styles
#     """
#     hungarian = HungarianRunSetting
#     korean1 = Korean1RunSetting


class AbstractTest(object):
    """
    Abstract class
    A test is a given list of runs
    """
    def __init__(self, listOfRuns):
        self.runs = listOfRuns


class AbstractRunSetting(object):
    """
    Parameters needed by a run for all styles
    """
    def __init__(self):
        self.trackLength = None
        self.maxTime = None
        self.eliminatingTime = None
        self.timeBonus = None
        self.maxTimeBonus = None
        self.timeMalus = None
        self.numberOfTargets  = None
        self.multipleArrowsPerTarget = None
        self.possibleValues = None
        self.targetBonus = None


class HungarianRunSetting(AbstractRunSetting):
    """
    Parameters for a hungarian run
    """
    def __init__(self):
        super(HungarianRunSetting, self).__init__()
        self.trackLength = 99
        self.maxTime = 20
        self.eliminatingTime = 20
        self.timeBonus = 1
        self.multipleArrowsPerTarget = True
        self.numberOfTargets = 1
        self.possibleValues = [2, 3, 4]

class Korean1RunSetting(AbstractRunSetting):
    """
    Parameters for a korean single shoot run
    """
    def __init__(self):
        super(Korean1RunSetting, self).__init__()
        self.trackLength = 90
        self.maxTime = 14
        self.timeBonus = 1
        self.timeMalus = 1
        self.multipleArrowsPerTarget = False
        self.numberOfTargets = 1
        self.possibleValues = [0, 1, 2, 3, 4, 5]


class Korean1RunSetting(AbstractRunSetting):
    """
    Parameters for a korean double shoot run
    """
    def __init__(self):
        super(Korean1RunSetting, self).__init__()
        self.trackLength = 90
        self.maxTime = 14
        self.timeBonus = 1
        self.timeMalus = 1
        self.multipleArrowsPerTarget = False
        self.numberOfTargets = 2
        self.possibleValues = [0, 1, 2, 3, 4, 5]
        self.targetBonus = [2]


class Run(object):
    """
    A run is associated to a competitor.
    Its settings are determined by its style.
    It has an id indicating its position inside a test.
    It contains the time value of the run, the target point,
    and can compute the target score and the total score for the run.

    """

    def __init__(self, styleSetting, runId, competitorId):
        self.setting = styleSetting
        self.runId = runId
        self.competitorId = competitorId
        self.time = None
        self.timeBonusGiven = True
        self.targetValues = None
        self.eliminated = False
        self.targetBonusGiven = False

    def timeScore(self):
        if self.time is not None:
            if self.setting.eliminatingTime is not None:
                if self.time > self.setting.eliminatingTime:
                    self.eliminated = True
                    return 0
            if self.time > self.setting.maxTime:
                return (self.setting.maxTime - self.time) * self.setting.timeMalus
            else:
                if self.timeBonusGiven:
                    return (self.setting.maxTime - self.time) * self.setting.timeBonus
                else:
                    return 0

    def targetScore(self):
        if self.targetValues is not None:
            ret = sum(self.targetValues)
            if self.targetBonusGiven:
                ret += self.setting.targetBonus[self.targetBonusGiven]
            return ret

    def score(self):
        timeSc = self.timeScore()
        if not self.eliminated:
            targetSc = self.targetScore()
            if targetSc:
                return max(0, timeSc + targetSc)
            else:
                return 0
        else:
            return 0

    def targetValuesFromString(self, targets_string):
        """
        Score can be both "nothing-separated" or comma-separated
        """
        if ',' in targets_string:
            targets_string = targets_string.split(",")
        self.targetValues = [int(i) for i in targets_string]
        return self.targetValues


class Competition(object):
    """
    A competition contains :
        - a list of competitors partitioned in groups
        - a competition style
        - an ensemble of runs associated to each competitors
    """
    def __init__(self, competitors, style):
        self.competitors = competitors
        self.runsDict = defaultdict(list)

    def addRun(self, competitor, run):
        # try :
        self.runsDict[competitor].append(run)
        #except KeyError:
        #    self.runsDict[competitor] = [run]
        return
