from dataclasses import dataclass
from enum import Enum
from typing import Type, Optional, TypeVar

from flet import dropdown, InputBorder

from .user_input import UserInputWidget, UserInput


EMPTY = "__EMPTY__"
EMPTY_TEXT = "---"
E = TypeVar('E', bound=Enum)


class EnumChoiceWidget(UserInputWidget[E], dropdown.Dropdown):
    enum_type: Type[E]

    @property
    def final_value(self) -> Optional[E]:
        return None if self.value == EMPTY else self.enum_type(self.value)

    def __init__(
            self,
            *,
            enum_type: Type[E] = None,
            **kwargs
    ):
        assert enum_type is not None
        self.enum_type = enum_type
        super().__init__(**kwargs)

        self.options = [
            dropdown.Option(key=x.value, text=x.name) for x in self.enum_type
        ]
        if not self.required:
            self.options.insert(0, dropdown.Option(key=EMPTY, text=EMPTY_TEXT))
        self.on_change = self.handle_value_change_and_update
        if self.in_table_cell:
            self.apply_in_table_cell_params()
        else:
            self.width = self.default_width

    def apply_in_table_cell_params(self):
        self.border = InputBorder.NONE
        self.content_padding = 0
        self.label = None

    def set_value(self, value: E, initial: bool = False):
        assert value is None or isinstance(value, Enum)
        if value is None:
            self.value = EMPTY
        else:
            self.value = value.value


@dataclass
class EnumChoice(UserInput[EnumChoiceWidget[E]]):
    enum_type: Type[E] = None

    @property
    def widget_type(self):
        return EnumChoiceWidget

    @property
    def default_initial(self) -> str | E:
        if self.required:
            return next(self.enum_type.__iter__())
