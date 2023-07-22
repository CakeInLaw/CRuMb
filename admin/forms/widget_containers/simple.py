from typing import Optional

from flet import Stack, Container, Text, border, padding

from .base import BaseWidgetContainer, W
from .tooltip import InputTooltip
from ..widgets import CheckboxWidget


class SimpleWidgetContainer(BaseWidgetContainer[W], Stack):
    def __init__(self, widget: W):
        super().__init__(
            widget=widget,
        )
        self.container = Container(
            content=InputTooltip(self.widget),
            border_radius=12,
        )
        self._label = Text(size=12, color='primary')
        self._label_container = Container(
            content=self._label,
            padding=padding.symmetric(horizontal=3),
            bgcolor='white',
            left=10,
            offset=(0, -0.5)
        )
        self.label = None
        self.controls = [self.container, self._label_container]

    def apply_widget_features(self):
        if isinstance(self.widget, CheckboxWidget):
            self.widget.label = self.widget.label_text
        else:
            self.label = self.widget.label_text
            self.container.border = border.all(2, 'primary'),

    @property
    def label(self) -> Text:
        return self._label

    @label.setter
    def label(self, v: Optional[str]):
        if v:
            self._label.value = v
            self._label_container.visible = True
        else:
            self._label.value = ''
            self._label_container.visible = False
