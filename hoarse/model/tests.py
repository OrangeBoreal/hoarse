import unittest
from hoarse.models import Run, Competitor, HungarianRunSetting, Competition


class CompetitionTest(unittest.TestCase):
    def test_compute_totals(self):
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

        c1 = Competitor("Athalie", 0, groupNumber=1, idxInGroup=0)
        c2 = Competitor("Bérénice", 1, groupNumber=1, idxInGroup=1)
        c3 = Competitor("Cléôpâtre", 2, groupNumber=1, idxInGroup=2)
        cList = [c1, c2, c3]

        #read mock run results
        scores = []

        for run in runs:
            rawScore, time = run.split(", ")
            scores.append((rawScore, float(time)))

        runSet = HungarianRunSetting()
        myCompetition = Competition(cList, runSet)

        #run the competition
        for i in range(3):
            for j in range(3):
                currentRun = Run(runSet, runId=i, competitorId=j)
                rawScore, time = scores[3 * i + j]
                currentRun.time = time
                currentRun.targetValuesFromString(rawScore)
                myCompetition.addRun(j, currentRun)

        #print results

        finalScores = []

        for c in myCompetition.competitors:
            scoresPerRun =  []
            for r in myCompetition.runsDict[c.id]:
                scoresPerRun.append(r.score())
            finalScores.append(scoresPerRun)

        self.assertEqual(
            finalScores,
            [
                [9, 9, 0],
                [6, 9, 9],
                [0, 0, 3],
            ]
        )


if __name__ == '__main__':
    unittest.main()
