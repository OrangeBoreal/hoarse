# Kivy
from kivy.clock import Clock
from kivy.properties import NumericProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout

# Hoarse
from hoarse.models import Competitor
from hoarse.libs.draggable import DraggableElement

# Relative imports
from .app import HoarseApp
from .mixins import FocusMixin


class CompetitorsManagementMenu(FocusMixin, FloatLayout):
    counter = NumericProperty(0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        def addMockContent(*args, **kwargs):
            # debug competitor management
            names = (
                "Athalie,Bérénice,Célestine,Diogène,Electre,Figaro,Genghis,Hippocrate,"
                "Iphigénie,Jocaste,Kevin,Ludwig,Melenas,Nausicaa,Ophélie,Phèdre,Rhéa,Sixtine,"
                "Terpsichore,Ulysse,Vulcain,Wilfried,Xénophon,Yoam,Zaccharie"
            ).split(",")
            #debug other purposes
            names = ("Athalie,Bérénice,Célestine").split(",")
            
            for name in names:
                self.add_competitor(name)

        Clock.schedule_once(addMockContent)

    @property
    def competitors(self):
        return sorted([
            line.competitor
            for line in self.ids['competitors_list'].children
        ], key=lambda competitor: competitor.id)

    def set_error_style(self, error=True):
        text_input = self.ids['competitor_input']
        text_input.foreground_color = (1, 0, 0, 1) if error else (0, 0, 0, 1)

    @property
    def next_group(self):
        group = self.counter // 5 + 1
        self.counter += 1
        return group

    def add_competitor(self, riderName):
        if riderName == "" or riderName in {competitor.riderName for competitor in self.competitors}:
            self.set_error_style(True)
        else:
            competitor_line = CompetitorLine(
                name=riderName, group=self.next_group,
                menu=self, grid_layout=self.ids["competitors_list"],
                float_layout=self.ids['drag_area'],
                should_scroll_callback=self.should_scroll,
                on_reorder=self.on_reorder
            )
            self.ids['competitors_list'].add_widget(competitor_line)
            self.ids['competitor_input'].text = ""

        self.setFocus(self.ids['competitor_input'])

    def remove_competitor(self, line):
        self.ids['competitors_list'].remove_widget(line)

    def validate(self):
        app = HoarseApp.get()
        app.competition.competitors = self.competitors

        app.switch_screen("style-menu")

    def should_scroll(self, speed):
        scroll_speed = 30
        scroll_view = self.ids["scroll_view"]
        scroll_y = scroll_view.convert_distance_to_scroll(0, speed * scroll_speed)[1]
        scroll_view.scroll_y += scroll_y
        scroll_view.scroll_y = max(min(scroll_view.scroll_y, 1), 0)

    def on_reorder(self):
        self.counter = 0
        for competitor in self.ids['competitors_list'].children[::-1]:
            competitor.group = self.next_group


class CompetitorLine(DraggableElement):

    group = NumericProperty(0)
    competitor = ObjectProperty(None)

    def __init__(self, name, group, menu, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.menu = menu
        self.ids["name"].text = name
        self.drag_button = self.ids["drag_button"]
        self.element = self.ids["content"]
        self.duration = 0.2
        self.competitor = Competitor(riderName=name, group=0)
        self.group = group

    def on_group(self, line, value=None):
        self.ids["competitorGroup"].text = "G{}".format(value)
        self.competitor.group = value

    def on_delete(self):
        self.menu.remove_competitor(self)
