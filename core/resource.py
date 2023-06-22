from typing import TYPE_CHECKING, Generic, TypeVar, Type

from .lists import ListView
from .forms import FormView

if TYPE_CHECKING:
    from .base_model import BaseModel


MODEL = TypeVar['MODEL', BaseModel]


class Resource(Generic[MODEL]):
    model: Type[MODEL]
    current_instance: MODEL

    def __init__(self, instance: MODEL) -> None:
        self.current_instance = instance

    def get_list(self) -> ListView:
        pass

    def _get_form(self, *, create: bool = True) -> FormView:
        pass

    def get_create_form(self):
        return self._get_form(create=True)

    def get_edit_form(self):
        return self._get_form(create=False)
