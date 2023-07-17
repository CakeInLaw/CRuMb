from dataclasses import dataclass, field
from typing import Any

from flet import Container

from core.orm import BaseModel
from core.types import BackFKData
from .object_input import ObjectInputWidget
from .user_input import UserInput, UserInputWidget
from .. import InputGroup
from ...exceptions import InputValidationError


class ObjectsArrayInputWidget(UserInputWidget[list[dict[str, Any]]], Container):

    @property
    def final_value(self) -> BackFKData:
        return {"add": [o.final_value for o in self.object_list]}

    def __init__(
            self,
            fields: list[UserInput | InputGroup],
            variant: str = 'table',
            **kwargs
    ):
        super().__init__(**kwargs)
        self.fields = fields
        self.variant = variant
        self.object_list: list[ObjectInputWidget] = []

    def _set_initial_value(self, value: list[BaseModel] | list[dict[str, Any]]) -> None:
        pass

    def has_changed(self) -> bool:
        return any([widget.has_changed() for widget in self.object_list])

    async def set_object_error(self, err: dict[str, Any]):
        if '__root__' in err:
            root = err.pop('__root__')
            # TODO
        for name, e in err.items():

            await self.fields_map[name].set_object_error(e)

    def is_valid(self) -> bool:
        has_error = False
        for widget in self.object_list:
            try:
                widget._validate()
            except InputValidationError:
                has_error = True
        return has_error

@dataclass
class ObjectsArrayInput(UserInput[ObjectsArrayInputWidget]):
    fields: list[UserInput | InputGroup] = field(default_factory=list)
    variant: str = 'table'

    @property
    def widget_type(self):
        return ObjectsArrayInputWidget

    def add_field(self, item: UserInput | InputGroup) -> None:
        self.fields.append(item)

    @property
    def default_initial(self) -> list[BaseModel] | list[dict[str, Any]]:
        return []
