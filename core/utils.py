import re
from typing import Any


def remove_extra_spaces(string: str) -> str:
    return remove_extra_spaces.pattern.sub(' ', string)


remove_extra_spaces.pattern = re.compile('\s+')


def default_if_none(value: Any, default: Any):
    if value is None:
        return default
    return value
