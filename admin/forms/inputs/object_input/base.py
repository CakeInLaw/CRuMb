from dataclasses import dataclass, field
from typing import Any, TypeVar

from flet import Container, Row, Column, Control

from core.orm import BaseModel
from admin.exceptions import InputValidationError
from admin.table import TableRow, TableCell
from ..user_input import UserInputWidget, UserInput, UndefinedValue
from ... import InputGroup


class ObjectInputBaseWidget(UserInputWidget[dict[str, Any]]):
    can_be_placed_in_table: bool = False
    children_in_table: bool

    @property
    def final_value(self) -> dict[str, Any]:
        return {
            field_name: widget.final_value
            for field_name, widget in self.fields_map.items()
        }

    def __init__(
            self,
            fields: list[UserInput | InputGroup],
            **kwargs
    ):
        super().__init__(**kwargs)
        self.fields = fields
        self.fields_map: dict[str, UserInputWidget] = {}

    def _create_widget(self, item: UserInput) -> UserInputWidget | Control:
        widget = item.widget(parent=self, initial=self.initial_for(item), in_table=self.children_in_table)
        self.fields_map[item.name] = widget
        return widget

    def get_widgets(self) -> list[Control]:
        widgets = []
        for f in self.fields:
            if isinstance(f, UserInput):
                widgets.append(self._create_widget(f))
            else:
                widgets.append(self._build_group(f))
        return widgets

    def _build_group(self, group: InputGroup) -> Control:
        controls: list[Control] = []
        for subgroup_or_input in group:
            if isinstance(subgroup_or_input, InputGroup):
                controls.append(self._build_group(subgroup_or_input))
            elif isinstance(subgroup_or_input, UserInput):
                controls.append(self._create_widget(subgroup_or_input))
        return group.to_control(controls)

    def initial_for(self, item: UserInput) -> Any:
        if self.initial_value is None:
            return UndefinedValue
        if isinstance(self.initial_value, dict):
            return self.initial_value.get(item.name, UndefinedValue)
        elif isinstance(self.initial_value, BaseModel):
            return getattr(self.initial_value, item.name, UndefinedValue)
        else:
            raise TypeError(f'Почему initial_value={type(self.initial_value)}, ({self.initial_value})?')

    def set_value(self, value: dict[str, Any], initial: bool = False):
        if initial:
            return
        assert isinstance(value, dict) and all(n in self.fields_map for n in value)
        for n, v in value.items():
            self.fields_map[n].set_value(v)

    def has_changed(self) -> bool:
        return any(widget.has_changed() for widget in self.fields_map.values())

    def is_valid(self) -> bool:
        valid = True
        for widget in self.fields_map.values():
            if not widget.is_valid():
                valid = False
        return valid

    def set_object_error(self, err: dict[str, Any]):
        if '__root__' in err:
            root = err.pop('__root__')
            # TODO
        for name, e in err.items():
            self.fields_map[name].set_object_error(e)


_OI = TypeVar('_OI', bound=ObjectInputBaseWidget)


@dataclass
class ObjectInputBase(UserInput[_OI]):
    fields: list[UserInput] = field(default_factory=list)

    def add_field(self, item: UserInput | InputGroup) -> None:
        self.fields.append(item)

    @property
    def default_initial(self) -> dict[str, Any]:
        return {}
