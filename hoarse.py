import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget

from kivy.properties import StringProperty,  ObjectProperty

class StyleButton(Button):
    name = StringProperty()


class StyleMenu(BoxLayout):
    pass

class SubstyleKoreanMenu(BoxLayout):
    pass

class CompetitorsManagementMenu(BoxLayout):
    pass

class HoarseApp(App):
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
