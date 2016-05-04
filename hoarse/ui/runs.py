# Kivy
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager

# Relative imports
from .app import HoarseApp
from .mixins import FocusMixin


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
            try:
                self.run.time = float(time)
            except ValueError:
                self.run.time = 0

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

    @staticmethod
    def configureTextInputs(settings, time, targets):
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

        visual_direction = {
            ('competitors', -1): "right",
            ('competitors', 1): "left",
            ('runs', -1): "down",
            ('runs', 1): "up",
        }[(next_by, direction)]

        if new_run != self.run:
            self.clear()
            new_screen = app.root.ids["run_screens"].toggle(visual_direction)
            new_screen.run = new_run
            new_screen.clear()

    def clear(self):
        self.ids["time_input"].text = ""
        self.ids["targets_input"].text = ""


class ToggleScreenManager(ScreenManager):

    @property
    def run_screen(self):
        return self.current_screen.children[0]

    def toggle(self, direction):
        self.transition.direction = direction
        new_screen = self.screens[int(not self.screens.index(self.current_screen))]
        self.current = new_screen.name
        return self.run_screen
