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
    
    
   # def dumpToCsv(self, filename):
        
    
    