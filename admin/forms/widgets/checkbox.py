from dataclasses import dataclass
from typing import Optional

import flet as ft

from .user_input import UserInputWidget, UserInput


class CheckboxWidget(UserInputWidget[bool], ft.Checkbox):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.on_change = self.handle_value_change_and_update
        if self.in_table_cell:
            self.apply_in_table_cell_params()

    def apply_in_table_cell_params(self):
        self.label = None

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
