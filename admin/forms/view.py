from contextvars import ContextVar
from typing import Any

from flet import Control


FormContext: ContextVar[dict[str, Any]] = ContextVar("FormContext", default=None)  # type: ignore


class FormView(Control):
    pass
