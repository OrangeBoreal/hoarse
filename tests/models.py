# Standard Library
import unittest

# Hoarse
from hoarse.models import Competition, CompetitionTest, Competitor, Run
from hoarse.models.rules import HungarianRunSettings, HungarianStyleSettings


class CompetitionTest(unittest.TestCase):
    def setUp(self):
        self.c1 = Competitor("Athalie", group=None)
        self.c2 = Competitor("Bérénice", group=None)
        self.c3 = Competitor("Cléôpâtre", group=None)
        competitors = [self.c1, self.c2, self.c3]

        HungarianRunSettings.numberOfRuns = 9

        self.competition = Competition()
        self.competition.competitors = competitors
        self.test = competition.addTest(HungarianStyleSettings())

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

        self.assertEqual(len(self.test.runSettings), 9)
        self.assertEqual(len(self.test.runs), 3 * 9)

        # Run the competition
        scores = getScores()
        for score, run in zip(scores, self.test.runs.values()):  # it's an ordered dict, so values are in the right orider
            targetScore, timeScore = score
            run.time = timeScore
            run.targetValuesFromString(targetScore)

        finalScores = self.test.getScoresPerCompetitor()
        # 3 contestants = 3 scores
        self.assertEqual(len(finalScores), 3)
        # Each score is mad of 9 runs
        self.assertTrue(all(len(score) == 9 for score in finalScores.values()))

        self.assertEqual(
            finalScores,
            {
                self.c1: [9, 9, 0] + [0] * 6,
                self.c2: [6, 9, 9] + [0] * 6,
                self.c3: [0, 0, 3] + [0] * 6,
            }
        )

        self.assertEqual(
            self.test.getScoresPerCompetitor(doSum=True),
            {
                self.c1: 18,
                self.c2: 24,
                self.c3: 3,
            }
        )


if __name__ == '__main__':
    unittest.main()
