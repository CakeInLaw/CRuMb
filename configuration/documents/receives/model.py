from datetime import datetime
from typing import TYPE_CHECKING, Union

from tortoise import fields
from core.orm import fields as orm_fields

from ..base_nomenclature_move_documents.model import MoveDocument, MoveDocumentValue

if TYPE_CHECKING:
    from configuration.directories.models import Provider
    from configuration.documents.models import ProviderReturn


__all__ = ["Receive", "ReceiveValue"]


class Receive(MoveDocument):
    """Документ приобретения товаров (ПТ)"""
    PREFIX: str = 'ПТ'

    provider: Union["Provider", fields.ForeignKeyRelation["Provider"]] = fields.ForeignKeyField(
        'directories.Provider', related_name='receives', on_delete=fields.RESTRICT
    )
    provider_doc_id: str = orm_fields.CharField(max_length=20)
    provider_doc_dt: datetime = fields.DatetimeField()

    values_list: list["ReceiveValue"] | fields.BackwardFKRelation["ReceiveValue"]
    returns: list["ProviderReturn"] | fields.BackwardFKRelation["ProviderReturn"]

    class Meta:
        table = 'doc__receives'
        ordering = ('dt',)


class ReceiveValue(MoveDocumentValue):
    count: float = orm_fields.FloatField(min_value=0)
    price: float = orm_fields.FloatField(min_value=0)
    doc: Union["Receive", fields.ForeignKeyRelation["Receive"]] = fields.ForeignKeyField(
        'documents.Receive', related_name='values_list', on_delete=fields.CASCADE
    )

    class Meta:
        table = 'doc__receives__values'
        ordering = 'ordering',
