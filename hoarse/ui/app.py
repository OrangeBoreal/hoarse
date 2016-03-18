# Kivy
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout

# Hoarse
from hoarse.models import Competition


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
