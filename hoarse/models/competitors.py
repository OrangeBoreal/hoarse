
# Hoarse
from hoarse.models.mixins import IDMixin
from hoarse.models.runs import Run
from hoarse.models.exceptions import NoMoreRuns


class Competitor(IDMixin):
    """
    Define the attributes of a competitor
    """
    def __init__(self, riderName, horseName=''):
        super().__init__()
        self.riderName = riderName
        self.horseName = horseName


class Entry(IDMixin):
    """
    An entry tracks a single competitor in a single test.
    """
    def __init__(self, competitor, group, test):
        self.competitor = competitor
        self.group = group
        self.test = test
        self.runs = []
        for runNumber, runSettings in enumerate(self.test.runSettings):
            self.runs.append(Run(
                runNumber=runNumber,
                runSettings=runSettings,
                entry=self,
            ))

        # self.retired = False

    @classmethod
    def enterTest(cls, competitor, group, test):
        entry = cls(competitor=competitor, group=group, test=test)
        return entry


class Group(object):
    def __init__(self, id):
        self.id = id
        self.entries = []

    @property
    def runs(self):
        """
        Iterates through all the runs but with the "natural" order:
         - first runs for all competitors ,
         - second runs for all competitors,
         - ...

        """
        # self.entries is the list of entries
        # each entry has a .run : the list of the runs for a competitor.
        # When we zip the entries we group together all the first runs,
        # then the second runs etc.

        # we have a kind of 2-dim matrix of runs by run number and by competitor
        # and zip() transposes this matrix.

        for nth_runs in zip(*(entry.runs for entry in self.entries)):
            for nth_run_for_competitor in nth_runs:
                yield nth_run_for_competitor
