from datetime import datetime
from typing import Union

from tortoise import fields
from core.orm import fields as orm_fields

from core.orm.base_model import BaseModel, ListValueModel


__all__ = ["Document", "DocumentListValue"]


class Document(BaseModel):
    """Базовый класс для всех документов"""

    PREFIX: str
    id: int = orm_fields.BigIntField(pk=True)
    conducted: bool = orm_fields.BooleanField(default=False)
    dt: datetime = orm_fields.DatetimeField()
    comment: str = orm_fields.TextField()

    @property
    def unique_number(self):
        return f'{self.PREFIX}-{self.id}'

    class Meta:
        abstract = True


class DocumentListValue(ListValueModel):
    """Базовая модель списка для документов"""
    doc: Union["Document", fields.ForeignKeyRelation["Document"]]

    class Meta:
        abstract = True
