from typing import Any
from contextvars import ContextVar

from flet import ListView as ListViewControl


ListContext: ContextVar[list[Any]] = ContextVar("ListContext", default=None)  # type: ignore


class ListView(ListViewControl):
    pass
