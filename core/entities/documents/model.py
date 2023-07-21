from datetime import datetime
from typing import Union

from tortoise import fields

from core.orm.base_model import BaseModel, RelatedListValueModel


__all__ = ["Document", "DocumentValue"]


class Document(BaseModel):
    """Базовый класс для всех документов"""

    PREFIX: str
    id: int = fields.BigIntField(pk=True)
    conducted: bool = fields.BooleanField(default=False)
    dt: datetime = fields.DatetimeField()
    comment: str = fields.TextField()

    class Meta:
        abstract = True


class DocumentValue(RelatedListValueModel):
    """Базовая модель списка для документов"""
    doc: Union["Document", fields.ForeignKeyRelation["Document"]]

    class Meta:
        abstract = True
