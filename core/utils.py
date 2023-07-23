import re
from typing import Any, TypeVar


def remove_extra_spaces(string: str) -> str:
    return remove_extra_spaces.pattern.sub(' ', string)


remove_extra_spaces.pattern = re.compile('\s+')


T = TypeVar('T')


def default_if_none(value: T, default: Any) -> T:
    if value is None:
        return default
    return value
