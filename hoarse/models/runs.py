# Hoarse
from hoarse.models.mixins import IDMixin


class Run(IDMixin):
    """
    A run is associated to a competitor.
    Its settings are determined by its style.
    It has an id indicating its position inside a test.
    It contains the time value of the run, the target point,
    and can compute the target score and the total score for the run.

    """

    def __init__(self, runNumber, runSettings, competitor):
        self.completed = False

        self.runSettings = runSettings
        self.runNumber = runNumber
        self.competitor = competitor
        self.time = None
        self.timeBonusGiven = True
        self.targetValues = None
        self.eliminated = False
        self.targetBonusGiven = False

    @property
    def displayRunNumber(self):
        return self.runNumber + 1

    def timeScore(self):
        if self.time is not None:
            if self.runSettings.eliminatingTime is not None:
                if self.time > self.runSettings.eliminatingTime:
                    self.eliminated = True
                    return 0
            if self.time > self.runSettings.maxTime:
                return (self.runSettings.maxTime - self.time) * self.runSettings.timeMalus
            else:
                if self.timeBonusGiven:
                    return (self.runSettings.maxTime - self.time) * self.runSettings.timeBonus
                else:
                    return 0

    def targetScore(self):
        if self.targetValues is not None:
            ret = sum(self.targetValues)
            if self.targetBonusGiven:
                ret += self.runSettings.targetBonus[self.targetBonusGiven]
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
