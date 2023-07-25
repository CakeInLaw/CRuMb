from dataclasses import dataclass
from typing import Optional

from flet import Row, Icon, Text, icons

from .user_input import UserInputWidget, UserInput
from ..widget_containers import BaseWidgetContainer, SimpleWidgetContainer


class CheckboxWidget(UserInputWidget[bool], Row):

    def __init__(self, **kwargs):
        Row.__init__(self)
        UserInputWidget.__init__(self, **kwargs)

        self.icon = Icon()
        self.label = Text(size=14, visible=False)
        self.color = 'primary' if not self.read_only else None
        self.controls = [self.icon, self.label]

        self.__finalize_init__()

    def apply_container(self, container: BaseWidgetContainer):
        super().apply_container(container)
        if isinstance(self.container, SimpleWidgetContainer):
            self.container.with_label = False
            self.container.with_border = False
            self.label.visible = True
            self.label.value = self.label_text

    @property
    def value(self) -> bool:
        return self._value

    @value.setter
    def value(self, v: bool):
        self._value = v
        if self._value:
            self.icon.name = icons.CHECK_BOX
        else:
            self.icon.name = icons.CHECK_BOX_OUTLINE_BLANK

    @property
    def color(self) -> Optional[str]:
        return self.icon.color

    @color.setter
    def color(self, v: Optional[str]):
        self.icon.color = v
        self.label.color = v

    @property
    def final_value(self) -> Optional[bool]:
        return self.value

    def set_value(self, value: bool, initial: bool = False):
        assert isinstance(value, bool)
        self.value = value

    def set_error_text(self, text: Optional[str]):
        super().set_error_text(text)
        if isinstance(self.container, SimpleWidgetContainer):
            self.color = 'error'

    def rm_error(self):
        super().rm_error()
        if isinstance(self.container, SimpleWidgetContainer):
            self.color = 'primary'

    async def start_change_event_handler(self, e=None):
        self.value = not self.value
        await super().start_change_event_handler(e)
        await super().end_change_event_handler(e)


@dataclass
class Checkbox(UserInput[CheckboxWidget]):

    @property
    def widget_type(self):
        return CheckboxWidget

    @property
    def default_initial(self) -> bool:
        return False
