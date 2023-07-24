from flet import Stack, Container, Text, border, padding

from .base import BaseWidgetContainer, W
from ..widgets import CheckboxWidget, InputWidget


class SimpleWidgetContainer(BaseWidgetContainer[W], Stack):
    def __init__(self, widget: W):
        BaseWidgetContainer.__init__(self, widget=widget)
        Stack.__init__(self)
        self.container = Container(
            content=self.widget_tooltip,
            border_radius=12,
        )
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
        self.apply_widget_features()

    def apply_widget_features(self):
        if isinstance(self.widget, CheckboxWidget):
            self.widget.label = self.widget.label_text
        else:
            self.container.border = border.all(2, 'primary')
        if isinstance(self.widget, InputWidget):
            self.widget.content_padding = 12
        if self.widget.container_width:
            self.container.width = self.widget.container_width

    def set_normal_borders(self):
        self.container.border = border.all(2, 'primary')

    def set_error_borders(self):
        self.container.border = border.all(2, 'error')

    def set_error_text(self, text: str):
        super().set_error_text(text)
        self.set_error_borders()
        if isinstance(self.widget, CheckboxWidget):
            self.widget.check_color = 'error'
        else:
            self._label.color = 'error'

    def rm_error(self):
        super().rm_error()
        self.set_normal_borders()
        if isinstance(self.widget, CheckboxWidget):
            self.widget.check_color = 'primary'
        else:
            self._label.color = 'primary'
