from typing import TYPE_CHECKING, Union, Optional, Literal
from dataclasses import dataclass, field

from flet import Control, Row, Column

if TYPE_CHECKING:
    from .inputs import UserInput


@dataclass
class InputGroup:
    fields: list[Union["UserInput", "InputGroup"], ...] = field(default_factory=list)
    label: Optional[str] = field(default=None)
    direction: Literal['horizontal', 'vertical'] = field(default='horizontal')

    def __iter__(self):
        return self.fields.__iter__()

    def to_control(self, children: list[Control]) -> Row | Column:
        if self.direction == 'horizontal':
            return Row(controls=children, spacing=30)
        else:
            return Column(controls=children)

    def add_field(self, item: Union["UserInput", "InputGroup"]) -> None:
        self.fields.append(item)


class FormSchema:
    groups: list[InputGroup]

    def __init__(self, *groups: Union["UserInput", "InputGroup"]):
        self.groups = []
        for group in groups:
            if isinstance(group, UserInput):
                self.groups.append(InputGroup([group]))
            elif isinstance(group, InputGroup):
                self.groups.append(group)

    def add_row(self, row: Union["UserInput", "InputGroup"]):
        if isinstance(row, InputGroup):
            self.groups.append(row)
        else:
            self.groups.append(InputGroup([row]))

    def __iter__(self):
        return self.groups.__iter__()
