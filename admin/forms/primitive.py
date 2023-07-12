from typing import Any, Optional

from . import inputs, InputGroup


PRIMITIVE_ITEM = str | tuple[str, dict[str, Any]] | dict[str, Any] | inputs.UserInput | InputGroup


class Primitive:
    values: list[PRIMITIVE_ITEM]

    def __init__(self, *values: PRIMITIVE_ITEM):
        self.values = list(values)

    def __iter__(self):
        return self.values.__iter__()

    def add(self, item: PRIMITIVE_ITEM):
        self.values.append(item)

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
