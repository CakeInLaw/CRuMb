from dataclasses import dataclass, field
from typing import Any

from .user_input import UserInput, UserInputWidget
from .. import InputGroup


class ObjectsArrayInputWidget(UserInputWidget[list[dict[str, Any]]]):
    pass


@dataclass
class ObjectsArrayInput(UserInput[ObjectsArrayInputWidget]):
    fields: list[UserInput] = field(default_factory=list)
    variant: str = 'table'

    @property
    def widget_type(self):
        return ObjectsArrayInputWidget

    def add_field(self, item: UserInput | InputGroup) -> None:
        self.fields.append(item)

    @property
    def default_initial(self) -> list[dict[str, Any]]:
        return []
