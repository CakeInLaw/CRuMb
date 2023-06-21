from datetime import datetime
from typing import TYPE_CHECKING, Union

from tortoise import fields
from tortoise.validators import MinValueValidator

from .nomenclature_move_documents import Document, DocumentValue

if TYPE_CHECKING:
    from configuration.directories.models import Provider
    from configuration.documents.models import ProviderReturn


__all__ = ["Receive", "ReceiveValue"]


class Receive(Document):
    """Документ приобретения товаров (ПТ)"""
    PREFIX: str = 'ПТ'

    provider: Union["Provider", fields.ForeignKeyRelation["Provider"]] = fields.ForeignKeyField(
        'models.Provider', related_name='receives', on_delete=fields.RESTRICT
    )
    provider_doc_id: str = fields.CharField(max_length=20)
    provider_doc_dt: datetime = fields.DatetimeField()

    values_list: list["ReceiveValue"] | fields.BackwardFKRelation["ReceiveValue"]
    returns: list["ProviderReturn"] | fields.BackwardFKRelation["ProviderReturn"]

    class Meta:
        table = 'doc__receives'
        ordering = ('dt',)


class ReceiveValue(DocumentValue):
    count: float = fields.FloatField(validators=[MinValueValidator(0)])
    price: float = fields.FloatField(validators=[MinValueValidator(0)])
    doc: Union["Receive", fields.ForeignKeyRelation["Receive"]] = fields.ForeignKeyField(
        'models.Receive', related_name='values_list', on_delete=fields.CASCADE
    )

    class Meta:
        table = 'doc__receives__values'
        ordering = ('order', )
