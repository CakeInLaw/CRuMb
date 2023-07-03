from dataclasses import dataclass
from enum import Enum
from typing import Type, Optional

from flet import dropdown

from admin.widgets.inputs.user_input import UserInputWidget, UserInput


EMPTY = "__EMPTY__"
EMPTY_TEXT = "---"


class EnumChoiceWidget(UserInputWidget[Enum], dropdown.Dropdown):
    enum_type: Type[Enum]

    def __init__(
            self,
            *,
            enum_type: Type[Enum] = None,
            **kwargs
    ):
        assert enum_type is not None
        self.enum_type = enum_type
        super().__init__(**kwargs)
        self.options = [
            dropdown.Option(key=x.value, text=x.name.title()) for x in self.enum_type
        ]
        if not self.required:
            self.options.insert(0, dropdown.Option(key=EMPTY, text=EMPTY_TEXT))

    def _set_initial_value(self, value: Optional[Enum]) -> None:
        self.value = None if value is None else value.value

    def to_value(self) -> Optional[Enum]:
        return None if self.value == EMPTY else self.enum_type(self.value)


@dataclass
class EnumChoice(UserInput[EnumChoiceWidget]):
    enum_type: Type[Enum] = None

    @property
    def widget_type(self):
        return EnumChoiceWidget
