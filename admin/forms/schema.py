from dataclasses import dataclass, field
from typing import Union, Optional, Literal

from flet import Control, Row, Column

from admin.widgets.inputs.user_input import UserInput


@dataclass
class InputGroup:
    fields: list[Union[UserInput, "InputGroup"], ...] = field(default_factory=list)
    label: Optional[str] = field(default=None)
    direction: Literal['horizontal', 'vertical'] = field(default='horizontal')

    def __iter__(self):
        return self.fields.__iter__()

    def to_control(self, controls: list[Control]) -> Control:
        if self.direction == 'horizontal':
            return Row(controls=controls, spacing=30)
        else:
            return Column(controls=controls)

    def add_field(self, item: Union[UserInput, "InputGroup"]) -> None:
        self.fields.append(item)


class FormSchema:
    groups: list[InputGroup]

    def __init__(self, *groups: UserInput | InputGroup):
        self.groups = []
        for group in groups:
            if isinstance(group, UserInput):
                self.groups.append(InputGroup([group]))
            elif isinstance(group, InputGroup):
                self.groups.append(group)
            else:
                raise ValueError(f'Не тот тип {type(group)}')

    def add_row(self, row: UserInput | InputGroup):
        if isinstance(row, UserInput):
            self.groups.append(InputGroup([row]))
        elif isinstance(row, InputGroup):
            self.groups.append(row)
        else:
            raise ValueError(f'row должно быть {UserInput} или {InputGroup}')

    def __iter__(self):
        return self.groups.__iter__()
