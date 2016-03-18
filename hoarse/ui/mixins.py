# Kivy
from kivy.clock import Clock


class FocusMixin(object):
    @staticmethod
    def setFocus(input_element):
        def _setFocus(time):  # pylint: disable=unused-argument
            input_element.focus = True

        Clock.schedule_once(_setFocus)
