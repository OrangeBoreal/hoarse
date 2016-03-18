from itertools import groupby


class TestResults(object):
    """
    Compute the results of a test, ie the ranking of all competitors per score
    """
    def __init__(self, test):
        self.test = test
        self.scoresPerCompetitors = test.getScoresPerCompetitor(doSum=True)

    def ranking(self):

        def score_get(element):
            return element[1]

        ranked = sorted(self.scoresPerCompetitors.items(), key=score_get, reverse=True)
        rank = 1

        for score, competitors in groupby(ranked, key=score_get):
            rank_at_start = rank
            for competitor_tuple in competitors:
                yield rank_at_start, competitor_tuple[0]
                rank += 1

    def dumpToCsv(self, filename):
        with open("%s.csv" % filename, 'w') as csvfile:
            csvfile.write("Rank, Rider name, Horse name, Score, Target points,")
            for runNumber in range(self.test.totalRunNumber):
                csvfile.write("Run %d time, Run %d target points" % (runNumber + 1, runNumber + 1))
            csvfile.write("\n")

            for rank, competitor in self.ranking():
                csvfile.write("%d, %s, %s, %f," % (
                    rank, competitor.riderName,
                    competitor.horseName, self.scoresPerCompetitors[competitor]
                ))
                for runNumber in range(self.test.totalRunNumber):
                    run = self.test.runs[(runNumber, competitor)]
                    try:
                        csvfile.write("%f," % (run.time))
                    except TypeError:
                        csvfile.write("NA,")
                    try:
                        csvfile.write("%f," % (run.targetScore()))
                    except TypeError:
                        csvfile.write("0,")
                csvfile.write("\n")
