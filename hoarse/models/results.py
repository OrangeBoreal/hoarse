# Hoarse
from hoarse.models.competitions import CompetitionTest


class TestResults(object):
    """
    Compute the results of a test, ie the ranking of all competitors per score
    """
    def __init__(self, test):
        self.test = test
        self.scoresPerCompetitors = test.getScoresPerCompetitor(doSum=True)

    def ranking(self):
        return [c for c in sorted(self.scoresPerCompetitors, key=self.scoresPerCompetitors.get, reverse=True)]

    def dumpToCsv(self, filename):
        rank = 1
        with open("%s.csv" % filename, 'w') as csvfile:
            csvfile.write("Rank, Rider name, Horse name, Score, Target points,")
            for i in range(self.test.totalRunNumber):
                csvfile.write("Run %d time, Run %d target points" % (i + 1, i + 1))
            csvfile.write("\n")
            ranking = self.ranking()
            for competitor in ranking:
                csvfile.write("%d, %s, %s, %f," % (
                    rank, competitor.riderName,
                    competitor.horseName, self.scoresPerCompetitors[competitor])
                )
                for i in range(self.test.totalRunNumber):
                    run = self.test.runs[(i, competitor)]
                    try:
                        csvfile.write("%f," % (run.time))
                    except TypeError:
                        csvfile.write("NA,")
                    try:
                        csvfile.write("%f," % (run.targetScore()))
                    except TypeError:
                        csvfile.write("0,")
                csvfile.write("\n")
