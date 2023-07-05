from dataclasses import dataclass
from typing import Optional

import flet as ft

from .user_input import UserInputWidget, UserInput


class CheckboxWidget(UserInputWidget[bool], ft.Checkbox):

    @property
    def final_value(self) -> Optional[bool]:
        return self.value

    def _set_initial_value(self, value: bool) -> None:
        self.value = bool(value)


@dataclass
class Checkbox(UserInput[CheckboxWidget]):

    @property
    def widget_type(self):
        return CheckboxWidget
