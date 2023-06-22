from typing import TYPE_CHECKING, Union, Optional
from datetime import datetime

from tortoise import fields
from tortoise.validators import MinValueValidator
from core.entities.info_registers import InfoRegister

from configuration.constants import DOCUMENT_REF_LEN

if TYPE_CHECKING:
    from configuration.directories.models import Nomenclature


__all__ = ["NomenclatureCost"]


class NomenclatureCost(InfoRegister):
    id: int = fields.BigIntField(pk=True)
    nomenclature: Union["Nomenclature", fields.ForeignKeyRelation["Nomenclature"]] = fields.ForeignKeyField(
        'directories.Nomenclature', related_name='cost', on_delete=fields.RESTRICT
    )
    document_ref: Optional[str] = fields.CharField(max_length=DOCUMENT_REF_LEN, null=True)
    cost: float = fields.FloatField(validators=[MinValueValidator(0)])
    count: float = fields.FloatField(validators=[MinValueValidator(0)])
    dt: datetime = fields.DatetimeField()

    class Meta:
        table = "info_register__nomenclature_costs"
        ordering = ("dt", )
