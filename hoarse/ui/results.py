# Kivy
from kivy.uix.boxlayout import BoxLayout

# Hoarse
from hoarse.models import TestResults


class ResultScreen(BoxLayout):
    def add_result(self, rank, name, score):
        result_line = ResultLine(rank=rank, name=name, score=score)
        self.ids['results_list'].add_widget(result_line)

    def print_results(self, test):
        results = TestResults(test)
        results.dumpToCsv("tmp")
        results.dumpRaw("raw")
        for rank, competitor, score, _ in results.ranking():
            self.add_result(rank=rank, name=competitor.riderName, score=score)


class ResultLine(BoxLayout):
    def __init__(self, rank, name, score):
        super().__init__()
        self.ids["rank"].text = "{}".format(rank)
        self.ids["name"].text = name
        self.ids["score"].text = "{}".format(score)
