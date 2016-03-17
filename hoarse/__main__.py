import kivy
from kivy.clock import Clock
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.graphics import Rectangle
from kivy.properties import StringProperty,  ObjectProperty, NumericProperty

from hoarse.models import Competition, Competitor, TestResults
from hoarse.models.rules import HungarianStyleSettings

class StyleButton(Button):
    name = StringProperty()

    names_to_settings = {"hungarian": HungarianStyleSettings}

    def validate(self, name):
        settings_class = self.names_to_settings[name]
        app = HoarseApp.get()
        test = app.competition.addTest(settings_class())

        run_screen = app.root.ids["run_screen"]

        run_screen.test = test
        run_screen.run = test.getFirstUncompletedRun()

        app.switch_screen("run-screen")

class StyleMenu(BoxLayout):
    pass

class SubstyleKoreanMenu(BoxLayout):
    pass

class RunScreen(FloatLayout):
    competitor_text = StringProperty()
    run_text = StringProperty()
    score_text = StringProperty()

    run = ObjectProperty()

    def setRun(self, run):
        self.run = run
        self.updateDisplay()

    def updateScore(self, targets, time):
        if self.run:
            self.run.targetValuesFromString(targets)
            self.run.time = float(time)
            self.on_run()

    def on_run(self, *args, **kwargs):
        self.updateDisplay()

    def updateDisplay(self):
        if self.run:
            self.competitor_text = self.run.competitor.riderName
            self.run_text = "Run {}".format(self.run.displayRunNumber)
            self.score_text = "Score : {}".format(self.run.score())

    def validate(self, by="competitors", direction=1):
        app = HoarseApp.get()
        try:
            new_run = app.competition.tests[0].getNextRun(self.run, by=by, direction=direction)
            if new_run != self.run:
                self.setRun(new_run)
        except app.competition.tests[0].NoMoreRuns:
            result_screen = app.root.ids["result_screen"]
            result_screen.print_results(app.competition.tests[0])
            app.switch_screen("result-screen")

class ResultScreen(BoxLayout):
    def add_result(self, rank, name, score):
        result_line = ResultLine(rank=rank, name=name, score=score)
        self.ids['results_list'].add_widget(result_line)

    def print_results(self, test):
        results = TestResults(test)
        results.dumpToCsv("tmp")
        rank = 1
        for competitor in results.ranking():
            self.add_result(rank=rank, name=competitor.riderName, score=results.scoresPerCompetitors[competitor])
            rank += 1


class ResultLine(BoxLayout):
    def __init__(self, rank, name, score):
        super().__init__()
        self.ids["rank"].text = "{}".format(rank)
        self.ids["name"].text = name
        self.ids["score"].text = "{}".format(score)



class CompetitorsManagementMenu(FloatLayout):
    counter = NumericProperty(0)

    def __init__(self, *args, **kwargs):
        """
        For now, the init method only adds static content so that you
        """
        super().__init__(*args, **kwargs)

        def addMockContent(*args, **kwargs):
            for name in ["Athalie", "Bérénice", "Célestine"]:
                self.add_competitor(name)

        Clock.schedule_once(addMockContent)

    @property
    def competitors(self):
        return [line.competitor for line in self.ids['competitors_list'].children]

    def add_competitor(self, riderName):
        text_input = self.ids['competitor_input']
        if riderName == "" or riderName in {competitor.riderName for competitor in self.competitors}:
            text_input.foreground_color = (1, 0, 0, 1)
        else:
            group = self.counter // 5 + 1
            self.counter += 1
            competitor_line = CompetitorLine(competitor=Competitor(riderName=riderName, group=group))
            self.ids['competitors_list'].add_widget(competitor_line)
            text_input.text = ""

        def setFocus(*args, **kwargs):
            self.ids['competitor_input'].focus = True

        Clock.schedule_once(setFocus)

    def validate(self):
        app = HoarseApp.get()
        app.competition.competitors = self.competitors

        app.switch_screen("style-menu")

class CompetitorLine(BoxLayout):
    def __init__(self, competitor):
        super().__init__()
        self.competitor = competitor
        self.ids["competitorGroup"].text = "G{}".format(competitor.group)
        self.ids["name"].text = competitor.riderName

class HoarseApp(App):
    competition = Competition()

    @classmethod
    def get(cls):
        return App.get_running_app()

    def build(self):
        return HoarseMain()

    @property
    def screen_manager(self):
        return self.root.ids["screen_manager"]

    def switch_screen(self, name):
        self.screen_manager.current = name


class HoarseMain(BoxLayout):
    screen_manager = ObjectProperty(None)


if __name__ == "__main__":
    HoarseApp().run()
