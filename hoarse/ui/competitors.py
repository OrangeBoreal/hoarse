# Kivy
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout

# Hoarse
from hoarse.models import Competitor

# Relative imports
from .app import HoarseApp
from .mixins import FocusMixin


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
