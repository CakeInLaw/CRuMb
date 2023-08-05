from typing import TYPE_CHECKING, Union

from tortoise import fields
from core.orm import fields as orm_fields

from core.entities.documents.model import Document, DocumentListValue

if TYPE_CHECKING:
    from configuration.directories.models import Nomenclature, PriceGroup


__all__ = ["PriceSetup", "PriceSetupValuesList"]


class PriceSetup(Document):
    """Документ установки цен (УЦ)"""

    PREFIX: str = 'УЦ'

    price_group_id: int
    price_group: Union["PriceGroup", fields.ForeignKeyRelation["PriceGroup"]] = fields.ForeignKeyField(
        'directories.PriceGroup', related_name='setups', on_delete=fields.RESTRICT
    )

    class Meta:
        table = "doc__price_setups"


class PriceSetupValuesList(DocumentListValue):

    owner: Union["PriceSetup", fields.ForeignKeyRelation["PriceSetup"]] = fields.ForeignKeyField(
        'documents.PriceSetup', related_name='values_list', on_delete=fields.CASCADE
    )
    nomenclature_id: int
    nomenclature: Union["Nomenclature", fields.ForeignKeyRelation["Nomenclature"]] = fields.ForeignKeyField(
        'directories.Nomenclature', on_delete=fields.RESTRICT
    )
    price: float = orm_fields.FloatField(min_value=0)

    class Meta:
        table = "doc__price_setups__values"
