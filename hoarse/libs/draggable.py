"""
Heavily inspired (a.k.a copy pasted) from
https://gist.github.com/tshirtman/7282822
with lots of modifications
"""

from kivy.app import App
from kivy.properties import ObjectProperty, NumericProperty
from kivy.clock import Clock

from hoarse.libs.magnet import Magnet


class DraggableElement(Magnet):
    """
    Represents an element that we can vertically drag.
    If it's in a scrollView, and should_scroll_callback is
    provided, it will call it with an argument "scroll_speed" (0<v<1)
    telling how much it should be scrolled (positive is upwards).

    element is the element we're wrapping.
    drag_button is an optionnal element if we want the drag
        behavior to be activated only if a specific part of
        the element is dragged
    grid_layout is the layout from which we're taking the element
    float_layout is a place where we can freely move our element
        during drag.
    scroll_frequency is the frequency for calling should_scroll_callback
    scroll_zone is the percentage of the size of the grid_layout that
        will trigger a scroll
    """
    element = ObjectProperty(None, allownone=True)
    drag_button = ObjectProperty(None)
    grid_layout = ObjectProperty(None)
    float_layout = ObjectProperty(None)
    placeholder = ObjectProperty(None)
    scroll_frequency = NumericProperty(1 / 30)
    scroll_zone = NumericProperty(1 / 5)

    def __init__(self, should_scroll_callback=None, on_reorder=None, *args, **kwargs):
        super(DraggableElement, self).__init__(*args, **kwargs)
        self.latest_touch = None
        self.should_scroll_callback = should_scroll_callback
        self.on_reorder = on_reorder

    def on_element(self, *args):
        self.clear_widgets()

        if self.element:
            Clock.schedule_once(lambda *x: self.add_widget(self.element), 0)

    def move_to_touch(self, touch):
        self.element.center_y = self.to_window(*touch.pos)[1]

    def on_touch_down(self, touch, *args):
        drag_element = self.drag_button or self

        if drag_element.collide_point(*touch.pos):
            touch.grab(self)
            old_x = self.to_window(*self.element.pos)[0]
            self.remove_widget(self.element)
            self.float_layout.add_widget(self.element)
            self.element.x = old_x
            self.move_to_touch(touch)

            self.latest_touch = touch
            Clock.schedule_interval(self.on_element_dragged, self.scroll_frequency)

            return True

        return super(DraggableElement, self).on_touch_down(touch, *args)

    def on_element_dragged(self, dt):
        if self.latest_touch is not None:
            if self.should_scroll_callback:
                touch_y = self.latest_touch.y
                top = self.float_layout.top
                bottom = self.float_layout.y
                float_height = self.float_layout.height
                zone_size = float_height * self.scroll_zone

                if touch_y < bottom + zone_size:
                    speed = (touch_y - (bottom + zone_size)) / zone_size
                    self.should_scroll_callback(max(speed, -1))

                if touch_y > top - zone_size:
                    speed = (touch_y - (top - zone_size)) / zone_size
                    self.should_scroll_callback(min(speed, 1))

        else:
            return False

    def on_touch_move(self, touch, *args):

        if touch.grab_current == self:
            self.move_to_touch(touch)

            self.grid_layout.remove_widget(self)

            topmost_child = self.grid_layout.children[-1]
            if touch.y > topmost_child.center_y:
                self.grid_layout.add_widget(self, len(self.grid_layout.children))
            else:
                for i, child in enumerate(self.grid_layout.children):
                    if touch.y < child.center_y:
                        self.grid_layout.add_widget(self, i)
                        break
                else:
                    self.grid_layout.add_widget(self)

            self.latest_touch = touch
        return super(DraggableElement, self).on_touch_move(touch, *args)

    def on_touch_up(self, touch, *args):
        if touch.grab_current == self:
            self.latest_touch = None
            self.element.x = 0
            self.element.center_y = touch.y
            self.float_layout.remove_widget(self.element)
            self.add_widget(self.element)
            touch.ungrab(self)
            if self.on_reorder:
                self.on_reorder()
            return True

        return super(DraggableElement, self).on_touch_up(touch, *args)
