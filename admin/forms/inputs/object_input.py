from dataclasses import dataclass, field
from typing import Any

from flet import Container, Row, Column, Control

from admin.exceptions import InputValidationError
from core.orm import BaseModel
from .user_input import UserInputWidget, UserInput, UndefinedValue
from .. import InputGroup


class ObjectInputWidget(UserInputWidget[dict[str, Any]], Container):
    can_handle_blur: bool = False

    def __init__(self, variant: str, fields: list[UserInput | InputGroup], **kwargs):
        super().__init__(**kwargs)
        self.variant = variant
        self.fields = fields
        self.fields_map: dict[str, UserInputWidget] = {}
        self.content = self.create_content()

    def create_content(self) -> Control:
        widgets = self.get_widgets()
        match self.variant:
            case 'row':
                return Row(widgets, wrap=True)
            case 'column':
                return Column(widgets)
            case _:
                raise ValueError(f'Варианта отображения "{self.variant}" не существует')

    def _create_widget(self, item: UserInput) -> UserInputWidget | Control:
        widget = item.widget(form=self.form, name_prefix=self.name, initial=self.initial_for(item))
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
        print(self.initial_value)
        if self.initial_value is None:
            return UndefinedValue
        if isinstance(self.initial_value, dict):
            return self.initial_value.get(item.name, UndefinedValue)
        elif isinstance(self.initial_value, BaseModel):
            return getattr(self.initial_value, item.name, UndefinedValue)
        else:
            raise TypeError(f'Почему initial_value={type(self.initial_value)}, ({self.initial_value})?')

    @property
    def final_value(self) -> dict[str, Any]:
        return {
            field_name: widget.final_value
            for field_name, widget in self.fields_map.items()
        }

    def _set_initial_value(self, value: dict[str, Any]) -> None:
        pass

    def has_changed(self) -> bool:
        changed = False
        for widget in self.fields_map.values():
            if widget.has_changed():
                changed = True
                break
        return changed

    async def validate(self, reraise: bool = False) -> None:
        has_error = False
        for widget in self.fields_map.values():
            try:
                await widget.validate(reraise=True)
            except InputValidationError:
                has_error = True
        if reraise and has_error:
            raise InputValidationError('Исправьте ошибки')

    async def set_object_error(self, err: dict[str, Any]):
        if '__root__' in err:
            root = err.pop('__root__')
            # TODO
        for name, e in err.items():
            await self.fields_map[name].set_object_error(e)


@dataclass
class ObjectInput(UserInput[ObjectInputWidget]):
    fields: list[UserInput] = field(default_factory=list)
    variant: str = field(default='row')

    @property
    def widget_type(self):
        return ObjectInputWidget

    def add_field(self, item: UserInput | InputGroup) -> None:
        self.fields.append(item)

    @property
    def default_initial(self) -> dict[str, Any]:
        return {}
