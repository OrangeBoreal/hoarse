import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput


from kivy.properties import StringProperty,  ObjectProperty

class StyleButton(Button):
    name = StringProperty()


class StyleMenu(BoxLayout):
    pass

class SubstyleKoreanMenu(BoxLayout):
    pass

class CompetitorsManagementMenu(BoxLayout):
    counter = 0
    def add_competitor(self, name):
        self.counter += 1
        self.ids['competitors_list'].add_widget(CompetitorLine(name=name))

class CompetitorLine(BoxLayout):
    def __init__(self, name):
        super().__init__()
        self.ids["name"].text = name

class CompetitorTextInput(TextInput):

    def on_text_validate(self):
        self.parent.add_competitor(name=self.text)

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
