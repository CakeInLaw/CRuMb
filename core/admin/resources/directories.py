from typing import TypeVar

from core.entities.directories import DirectoryRepository

from core.admin.forms import DirectoryInputForm
from core.admin.resources.crud_resource import CrudResource


REP = TypeVar("REP", bound=DirectoryRepository)


class DirectoryResource(CrudResource[REP]):
    model_form = DirectoryInputForm
