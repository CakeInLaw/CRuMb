from typing import TYPE_CHECKING

from tortoise import fields

from core.entities.directories.model import Directory

if TYPE_CHECKING:
    from configuration.directories.models import Customer
    from configuration.info_registers.models import NomenclaturePrice


__all__ = ["PriceGroup"]


class PriceGroup(Directory):
    id: int = fields.IntField(pk=True)
    name: str = fields.CharField(max_length=50)

    customers: list["Customer"] | fields.BackwardFKRelation["Customer"]
    prices: list["NomenclaturePrice"] | fields.BackwardFKRelation["NomenclaturePrice"]

    class Meta:
        table = "dir__price_groups"
        ordering = ('id',)
