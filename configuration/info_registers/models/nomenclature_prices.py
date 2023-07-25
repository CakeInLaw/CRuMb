from typing import TYPE_CHECKING, Union
from datetime import datetime

from tortoise import fields
from core.orm import fields as orm_fields
from core.entities.info_registers.model import InfoRegister

from configuration.constants import DOCUMENT_REF_LEN

if TYPE_CHECKING:
    from configuration.directories.models import Nomenclature, PriceGroup


__all__ = ["NomenclaturePrice"]


class NomenclaturePrice(InfoRegister):
    id: int = orm_fields.BigIntField(pk=True)
    nomenclature: Union["Nomenclature", fields.ForeignKeyRelation["Nomenclature"]] = fields.ForeignKeyField(
        'directories.Nomenclature', related_name='prices', on_delete=fields.RESTRICT
    )
    document_ref: str = orm_fields.CharField(max_length=DOCUMENT_REF_LEN)
    price: float = orm_fields.FloatField(min_value=0)
    price_group: Union["PriceGroup", fields.ForeignKeyRelation["PriceGroup"]] = fields.ForeignKeyField(
        'directories.PriceGroup', related_name='prices', on_delete=fields.CASCADE
    )
    dt: datetime = fields.DatetimeField()

    class Meta:
        table = "reg_info__nomenclature_prices"
        ordering = ('dt',)
