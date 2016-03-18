# Standard Library
import unittest

# Hoarse
from hoarse.models import Competition, CompetitionTest, Competitor, Run
from hoarse.models.rules import HungarianStyleSettings


class CompetitionTest(unittest.TestCase):
    def test_compute_totals(self):

        def getScores():
            runs = [
                "223, 18",
                "3, 17",
                "2, 21",
                "223, 18",
                "3, 14",
                "2, 21",
                ", 18",
                "33, 17",
                "2, 19",
            ]
            for run in runs:
                rawScore, time = run.split(", ")
                yield rawScore, float(time)

        c1 = Competitor("Athalie", group=None)
        c2 = Competitor("Bérénice", group=None)
        c3 = Competitor("Cléôpâtre", group=None)
        competitors = [c1, c2, c3]

        competition = Competition(competitors=competitors)
        test = competition.addTest(HungarianStyleSettings())

        self.assertEqual(len(test.runSettings), 9)
        self.assertEqual(len(test.runs), 3 * 9)

        #run the competition
        scores = getScores()
        for score, run in zip(scores, test.runs.values()):  # it's an ordered dict, so values are in the right orider
            targetScore, timeScore = score
            run.time = timeScore
            run.targetValuesFromString(targetScore)

        finalScores = test.getScoresPerCompetitor()
        # 3 contestants = 3 scores
        self.assertEqual(len(finalScores), 3)
        # Each score is mad of 9 runs
        self.assertTrue(all(len(score) == 9 for score in finalScores.values()))

        self.assertEqual(
            finalScores,
            {
                c1: [9, 9, 0] + [0] * 6,
                c2: [6, 9, 9] + [0] * 6,
                c3: [0, 0, 3] + [0] * 6,
            }
        )

        self.assertEqual(
            test.getScoresPerCompetitor(doSum=True),
            {
                c1: 18,
                c2: 24,
                c3: 3,
            }
        )

if __name__ == '__main__':
    unittest.main()
