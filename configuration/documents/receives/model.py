from datetime import datetime
from typing import TYPE_CHECKING, Union

from tortoise import fields
from core.orm import fields as orm_fields

from ..base_nomenclature_move_documents.model import MoveDocument, MoveDocumentValuesList

if TYPE_CHECKING:
    from configuration.directories.models import Provider
    from configuration.documents.models import ProviderReturn


__all__ = ["Receive", "ReceiveValuesList"]


class Receive(MoveDocument):
    """Документ приобретения товаров (ПТ)"""
    PREFIX: str = 'ПТ'

    provider: Union["Provider", fields.ForeignKeyRelation["Provider"]] = fields.ForeignKeyField(
        'directories.Provider', related_name='receives', on_delete=fields.RESTRICT
    )
    provider_doc_id: str = orm_fields.CharField(max_length=20)
    provider_doc_dt: datetime = orm_fields.DatetimeField(null=True)

    values_list: list["ReceiveValuesList"] | fields.BackwardFKRelation["ReceiveValuesList"]
    returns: list["ProviderReturn"] | fields.BackwardFKRelation["ProviderReturn"]

    class Meta:
        table = 'doc__receives'

    def __str__(self):
        return f'Поступление {self.unique_number}'


class ReceiveValuesList(MoveDocumentValuesList):
    price: float = orm_fields.FloatField(min_value=0)
    owner: Union["Receive", fields.ForeignKeyRelation["Receive"]] = fields.ForeignKeyField(
        'documents.Receive', related_name='values_list', on_delete=fields.CASCADE
    )

    class Meta:
        table = 'doc__receives__values'
