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

class HoarseApp(App):
    def build(self):
        return HoarseMain()

class HoarseMain(BoxLayout):
    manager = ObjectProperty(None)


if __name__ == "__main__":
    HoarseApp().run()
