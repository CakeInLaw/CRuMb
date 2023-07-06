from typing import Any, Optional, Union

from admin.forms.schema import InputGroup
from admin.widgets import inputs

PRIMITIVE_ITEM = str | tuple[str, dict[str, Any]] | dict[str, Any] | inputs.UserInput | InputGroup
PRIMITIVE = list[PRIMITIVE_ITEM]


class Primitive:
    values: PRIMITIVE

    def __init__(self, values: Union[PRIMITIVE,  "Primitive"]):
        self.values = values.values if isinstance(values, Primitive) else values

    def __get__(self, instance, owner):
        return self.values

    @staticmethod
    def describe(item: str | tuple[str, dict[str, Any]]) -> tuple[str, Optional[dict[str, Any]]]:
        pass

    @staticmethod
    def is_field_name(item: PRIMITIVE_ITEM) -> bool:
        return isinstance(item, str)

    @staticmethod
    def is_field_with_extra(item: PRIMITIVE_ITEM) -> bool:
        return (
                isinstance(item, tuple)
                and len(item) == 2
                and isinstance(item[0], str)
                and isinstance(item[1], dict)
        )

    @staticmethod
    def is_schema(item: PRIMITIVE_ITEM) -> bool:
        return isinstance(item, (inputs.UserInput, InputGroup))

    @staticmethod
    def is_group(item: PRIMITIVE_ITEM) -> bool:
        return isinstance(item, dict) and 'fields' in item
