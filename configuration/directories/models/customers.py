from typing import TYPE_CHECKING, Union

from tortoise import fields
from core.directories.model import Directory

if TYPE_CHECKING:
    from configuration.directories.models import CustomerLocations, PriceGroup


__all__ = ["Customer"]


class Customer(Directory):
    id: int = fields.IntField(pk=True)
    name: str = fields.CharField(max_length=50)
    register_address: str = fields.CharField(max_length=200)

    customer_locations: list["CustomerLocations"] | fields.BackwardFKRelation["CustomerLocations"]
    price_group: Union["PriceGroup", fields.ForeignKeyNullableRelation["PriceGroup"]] = fields.ForeignKeyField(
        'models.PriceGroup', related_name='customers', on_delete=fields.RESTRICT
    )

    class Meta:
        table = "dir__customers"
        ordering = ('id',)
