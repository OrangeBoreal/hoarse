# Kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import NumericProperty, ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.screenmanager import ScreenManager

# Hoarse
from hoarse.models import Competition, Competitor, TestResults
from hoarse.models.rules import HungarianStyleSettings


class StyleButton(Button):
    name = StringProperty()

    names_to_settings = {"hungarian": HungarianStyleSettings}

    def validate(self, name):
        settings_class = self.names_to_settings[name]
        app = HoarseApp.get()
        test = app.competition.addTest(settings_class())

        run_screen = app.root.ids["run_screens"].run_screen

        run_screen.test = test
        run_screen.run = test.getFirstUncompletedRun()

        app.switch_screen("run-screens")


class StyleMenu(BoxLayout):
    pass


class SubstyleKoreanMenu(BoxLayout):
    pass


class FocusMixin(object):
    def setFocus(self, input):
        def _setFocus(__):
            input.focus = True

        Clock.schedule_once(_setFocus)


class RunScreen(FocusMixin, FloatLayout):
    competitor_text = StringProperty()
    run_text = StringProperty()
    score_text = StringProperty()

    run = ObjectProperty()
    style = ObjectProperty()

    def on_enter(self):
        self.setFocus(self.ids["time_input"])

    def on_run(self, *args):
        self.updateDisplay()

    def updateScore(self, targets, time):
        if self.run:
            self.run.targetValuesFromString(targets)
            self.run.time = float(time)

    def targets_filter(self, substring, undo=False):
        return substring if substring in self.run.runSettings.possibleStringValues else ""

    def updateDisplay(self):
        if self.run:
            self.competitor_text = self.run.competitor.riderName
            self.run_text = "Run {}".format(self.run.displayRunNumber)
            self.score_text = "Score : {}".format(self.run.score())
            self.configureTextInputs(
                settings=self.run.runSettings,
                targets=self.ids["targets_input"],
                time=self.ids["time_input"],
            )

    def configureTextInputs(self, settings, time, targets):
        time.hint_text = "{}".format(settings.maxTime or 0.)
        targets.hint_text = "".join(settings.possibleStringValues or "")

    def validate(self, next_by="competitors", direction=1):
        app = HoarseApp.get()
        try:
            new_run = app.competition.tests[0].getNextRun(self.run, next_by=next_by, direction=direction)
        except app.competition.tests[0].NoMoreRuns:
            result_screen = app.root.ids["result_screen"]
            result_screen.print_results(app.competition.tests[0])
            app.switch_screen("result-screen")
            return

        visual_directon = {
            ('competitors', -1): "right",
            ('competitors', 1): "left",
            ('runs', -1): "down",
            ('runs', 1): "up",
        }[(next_by, direction)]

        if new_run != self.run:
            self.clear()
            new_screen = app.root.ids["run_screens"].toggle(visual_directon)
            new_screen.run = new_run
            new_screen.clear()

    def clear(self):
        self.ids["time_input"].value = ""
        self.ids["targets_input"].value = ""


class ResultScreen(BoxLayout):
    def add_result(self, rank, name, score):
        result_line = ResultLine(rank=rank, name=name, score=score)
        self.ids['results_list'].add_widget(result_line)

    def print_results(self, test):
        results = TestResults(test)
        results.dumpToCsv("tmp")
        for rank, competitor in results.ranking():
            self.add_result(rank=rank, name=competitor.riderName, score=results.scoresPerCompetitors[competitor])


class ToggleScreenManager(ScreenManager):

    @property
    def run_screen(self):
        return self.current_screen.children[0]

    def toggle(self, direction):
        self.transition.direction = direction
        new_screen = self.screens[int(not self.screens.index(self.current_screen))]
        self.current = new_screen.name
        return self.run_screen


class ResultLine(BoxLayout):
    def __init__(self, rank, name, score):
        super().__init__()
        self.ids["rank"].text = "{}".format(rank)
        self.ids["name"].text = name
        self.ids["score"].text = "{}".format(score)


class SettingsMenu(StackLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        field = SettingField("nruns", "Number of runs", 0)
        self.add_widget(field)


class HungarianSettingsMenu(SettingsMenu):
    def setValues(self, styleSettings):
        self.ids['nruns'].setValue(styleSettings.numberOfRuns)


class SettingField(BoxLayout):
    def __init__(self, i, text, defaultValue):
        super().__init__()
        self.id = i
        self.ids["text"].text = text
        self.ids["val"].text = "{}".format(defaultValue)

    def setValue(self, val):
        self.ids["val"].text = "{}".format(val)


class CompetitorsManagementMenu(FocusMixin, FloatLayout):
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
        return sorted([
            line.competitor
            for line in self.ids['competitors_list'].children
        ], key=lambda competitor: competitor.id)

    def add_competitor(self, riderName):
        text_input = self.ids['competitor_input']
        if riderName == "" or riderName in {competitor.riderName for competitor in self.competitors}:
            text_input.foreground_color = (1, 0, 0, 1)
        else:
            group = self.counter // 5 + 1
            self.counter += 1
            competitor_line = CompetitorLine(
                competitor=Competitor(riderName=riderName, group=group)
            )
            self.ids['competitors_list'].add_widget(competitor_line)
            text_input.text = ""

        self.setFocus(self.ids['competitor_input'])

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


class HoarseMain(BoxLayout):
    screen_manager = ObjectProperty(None)


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


if __name__ == "__main__":
    HoarseApp().run()
