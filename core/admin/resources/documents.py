from typing import TypeVar

from core.admin.forms.widgets import Checkbox
from core.entities.documents import DocumentRepository

from core.admin.forms import DocumentInputForm
from core.admin.resources.crud_resource import CrudResource


REP = TypeVar("REP", bound=DocumentRepository)

ConductedFieldSchema = Checkbox(name='conducted', label='?', width=40, editable=False)


class DocumentResource(CrudResource[REP]):
    model_form = DocumentInputForm

    async def get_list_primitive(self):
        primitive = await super().get_list_primitive()
        if not primitive.has('conducted'):
            return primitive.copy().add(ConductedFieldSchema, 0)
        return primitive

    async def get_choice_primitive(self):
        primitive = await super().get_choice_primitive()
        if not primitive.has('conducted'):
            return primitive.copy().add(ConductedFieldSchema, 0)
        return primitive
