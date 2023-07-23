from dataclasses import dataclass
from typing import Optional

from flet import Checkbox

from .user_input import UserInputWidget, UserInput


class CheckboxWidget(UserInputWidget[bool], Checkbox):

    def __init__(self, **kwargs):
        Checkbox.__init__(self)
        UserInputWidget.__init__(self, **kwargs)

        self.on_focus = self.start_change_event_handler
        self.on_blur = self.end_change_event_handler

    @property
    def final_value(self) -> Optional[bool]:
        return self.value

    def set_value(self, value: bool, initial: bool = False):
        assert isinstance(value, bool)
        self.value = value


@dataclass
class Checkbox(UserInput[CheckboxWidget]):

    @property
    def widget_type(self):
        return CheckboxWidget

    @property
    def default_initial(self) -> bool:
        return False
