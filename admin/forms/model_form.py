from typing import Type

from core.repository import Repository
from .form import Form
from .schema import FormSchema


class ModelForm(Form):
    repository: Type[Repository]
    LANG: str
    create: bool
    create_schema: FormSchema = None
    edit_schema: FormSchema = None

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

    def get_form_schema(self) -> FormSchema:
        if self.create:
            form_schema = self.get_create_schema()
        else:
            form_schema = self.get_edit_schema()
        assert form_schema
        return form_schema

    def get_create_schema(self):
        schema = self.create_schema or self.form_schema
        if schema is None:
            self.form_schema = schema = form_factory(self.repository)
        return schema

    def get_edit_schema(self):
        return self.form_schema


def form_factory(repository: Type[Repository]) -> FormSchema:
    pass
