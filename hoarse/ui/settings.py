# Kivy
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.stacklayout import StackLayout

# Hoarse
from hoarse.models.rules import HungarianStyleSettings

# Relative imports
from .app import HoarseApp


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


class SettingsMenu(StackLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        field = SettingField("nruns", "Number of runs", 0)
        self.add_widget(field)


class SubstyleKoreanMenu(BoxLayout):
    pass


class HungarianSettingsMenu(SettingsMenu):
    def setValues(self, styleSettings):
        self.ids['nruns'].setValue(styleSettings.numberOfRuns)


class SettingField(BoxLayout):
    def __init__(self, id_, text, defaultValue):
        super().__init__()
        self.id = id_
        self.ids["text"].text = text
        self.ids["val"].text = "{}".format(defaultValue)

    def setValue(self, val):
        self.ids["val"].text = "{}".format(val)
