from flet import Stack, Container, GestureDetector, Text, border, padding, MouseCursor

from .base import BaseWidgetContainer, W


class SimpleWidgetContainer(BaseWidgetContainer[W], Stack):
    def __init__(self, widget: W):
        BaseWidgetContainer.__init__(self, widget=widget)
        Stack.__init__(self)

        self.container = Container(border_radius=12)
        if self.widget.editable:
            self.gesture_detector = GestureDetector(
                content=self.widget_tooltip,
                mouse_cursor=MouseCursor.CLICK
            )
            self.gesture_detector.on_tap_up = self.widget.start_change_event_handler
            self.container.content = self.gesture_detector
        else:
            self.container.content = self.widget_tooltip

        self._label = Text(
            value=self.widget.label_text or '',
            size=12,
            color='primary'
        )
        self._label_container = Container(
            content=self._label,
            padding=padding.symmetric(horizontal=3),
            bgcolor='background',
            left=10,
            offset=(0, -0.5),
            visible=not not self.widget.label_text
        )
        self.controls = [self.container, self._label_container]
        self.widget.apply_container(self)

    def set_width(self, v: int | float):
        self.container.width = v

    def get_width(self) -> int | float:
        return self.container.width

    def set_height(self, v: int | float):
        self.container.height = v

    def get_height(self) -> int | float:
        return self.container.height

    @property
    def with_label(self) -> bool:
        return self._label.visible

    @with_label.setter
    def with_label(self, v: bool):
        self._label.visible = v

    @property
    def with_border(self) -> bool:
        return self._with_border

    @with_border.setter
    def with_border(self, v: bool):
        self._with_border = v
        if self._with_border:
            self.set_normal_borders()
        else:
            self.container.border = None

    def set_normal_borders(self):
        self.container.border = border.all(2, 'primary')

    def set_error_borders(self):
        self.container.border = border.all(2, 'error')

    def set_error_text(self, text: str):
        super().set_error_text(text)
        if self.with_border:
            self.set_error_borders()
        if self.with_label:
            self._label.color = 'error'

    def rm_error(self):
        super().rm_error()
        if self.with_border:
            self.set_normal_borders()
        if self.with_label:
            self._label.color = 'primary'
