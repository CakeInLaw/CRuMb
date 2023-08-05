from typing import TYPE_CHECKING, Union

from tortoise import fields
from core.orm import fields as orm_fields

from core.entities.info_registers.model import InfoRegister, InfoRegisterResult

if TYPE_CHECKING:
    from configuration.directories.models import Nomenclature


__all__ = ["NomenclatureCost", "NomenclatureCostResult"]


class NomenclatureCost(InfoRegister):
    nomenclature: Union["Nomenclature", fields.ForeignKeyRelation["Nomenclature"]] = fields.ForeignKeyField(
        'directories.Nomenclature', related_name='cost_history', on_delete=fields.CASCADE
    )
    registrator: str = orm_fields.CharField(max_length=20)
    cost: float = orm_fields.FloatField(min_value=0)
    count: float = orm_fields.FloatField(min_value=0)

    class Meta:
        table = "info_register__nomenclature_costs"


class NomenclatureCostResult(InfoRegisterResult):
    nomenclature: Union["Nomenclature", fields.OneToOneRelation["Nomenclature"]] = fields.OneToOneField(
        'directories.Nomenclature', related_name='cost', on_delete=fields.CASCADE
    )
    cost: float = orm_fields.FloatField(min_value=0)

    class Meta:
        table = "info_register__nomenclature_costs__result"
