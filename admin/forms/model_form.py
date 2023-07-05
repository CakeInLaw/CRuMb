from typing import Type

from core.repository import Repository
from .form import Form


class ModelForm(Form):
    repository: Type[Repository]
    LANG: str
    create: bool

    def __init__(
            self,
            repository: Type[Repository],
            lang: str,
            create: bool
    ):
        super().__init__()
        self.repository = repository
        self.LANG = lang
        self.create = create


def model_form_factory(repository: Type[Repository]) -> Type[ModelForm]:
    pass
