from typing import TYPE_CHECKING, Union

from tortoise import fields
from core.orm import fields as orm_fields
from core.entities.info_registers.model import InfoRegister, InfoRegisterResult

if TYPE_CHECKING:
    from configuration.directories.models import Nomenclature, PriceGroup


__all__ = ["NomenclaturePrice", "NomenclaturePriceResult"]


class NomenclaturePrice(InfoRegister):
    nomenclature: Union["Nomenclature", fields.ForeignKeyRelation["Nomenclature"]] = fields.ForeignKeyField(
        'directories.Nomenclature', related_name='prices_history', on_delete=fields.RESTRICT
    )
    price_group: Union["PriceGroup", fields.ForeignKeyRelation["PriceGroup"]] = fields.ForeignKeyField(
        'directories.PriceGroup', related_name='prices_history', on_delete=fields.CASCADE
    )
    price: float = orm_fields.FloatField(min_value=0)

    class Meta:
        table = "info_register__nomenclature_prices"


class NomenclaturePriceResult(InfoRegisterResult):
    nomenclature: Union["Nomenclature", fields.ForeignKeyRelation["Nomenclature"]] = fields.ForeignKeyField(
        'directories.Nomenclature', related_name='prices', on_delete=fields.RESTRICT
    )
    price_group: Union["PriceGroup", fields.ForeignKeyRelation["PriceGroup"]] = fields.ForeignKeyField(
        'directories.PriceGroup', related_name='prices', on_delete=fields.CASCADE
    )
    price: float = orm_fields.FloatField(min_value=0)

    class Meta:
        table = "info_register__nomenclature_prices__result"
        unique_together = ('nomenclature', 'price_group')
