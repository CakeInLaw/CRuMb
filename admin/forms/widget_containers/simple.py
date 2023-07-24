from flet import Stack, Container, Text, border, padding

from .base import BaseWidgetContainer, W


class SimpleWidgetContainer(BaseWidgetContainer[W], Stack):
    def __init__(self, widget: W):
        BaseWidgetContainer.__init__(self, widget=widget)
        Stack.__init__(self)
        self.container = Container(
            content=self.widget_tooltip,
            border_radius=12,
        )
        if self.widget.editable and not self.widget.read_only:
            self.container.on_click = self.widget.start_change_event_handler
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

    def set_height(self, v: int | float):
        self.container.height = v

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
