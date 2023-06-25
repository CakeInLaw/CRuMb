from typing import TYPE_CHECKING, Generic, TypeVar, Type

from core.repository import Repository
from .lists import ListView
from .forms import FormView

if TYPE_CHECKING:
    from .app import CRuMbAdmin


REPOSITORY = TypeVar('REPOSITORY', bound=Repository)


class Resource(Generic[REPOSITORY]):
    repo: Type[REPOSITORY]
    ru_name: str
    app: "CRuMbAdmin"

    def __init__(self, app: "CRuMbAdmin") -> None:
        self.app = app

    def get_list(self) -> ListView:
        pass

    def _get_form(self, *, create: bool = True) -> FormView:
        pass

    def get_create_form(self):
        return self._get_form(create=True)

    def get_edit_form(self):
        return self._get_form(create=False)

    def delete(self):
        pass
