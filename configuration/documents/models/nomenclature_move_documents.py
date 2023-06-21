from typing import TYPE_CHECKING, Union

from tortoise import fields
from core.documents.model import Document as BaseDocument, DocumentValue as BaseDocumentValue

if TYPE_CHECKING:
    from configuration.directories.models import Employee, Nomenclature


__all__ = ["Document", "DocumentValue"]


class Document(BaseDocument):
    """Базовая модель для всех документов движения"""

    owner: Union["Employee", fields.ForeignKeyRelation["Employee"]] = fields.ForeignKeyField(
        'directories.Employee', on_delete=fields.RESTRICT
    )

    class Meta:
        abstract = True


class DocumentValue(BaseDocumentValue):
    """Базовая модель списка для документов движения номенклатуры"""

    nomenclature: Union["Nomenclature", fields.ForeignKeyRelation["Nomenclature"]] = fields.ForeignKeyField(
        'directories.Nomenclature', on_delete=fields.RESTRICT
    )

    class Meta:
        abstract = True
