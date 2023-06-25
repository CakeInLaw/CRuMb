from typing import TYPE_CHECKING, Union

from tortoise import fields

from core.entities.directories.model import Directory

if TYPE_CHECKING:
    from configuration.directories.models import CustomerLocation, PriceGroup


__all__ = ["Customer"]


class Customer(Directory):
    id: int = fields.IntField(pk=True)
    name: str = fields.CharField(max_length=50)
    register_address: str = fields.CharField(max_length=200)

    customer_locations: list["CustomerLocation"] | fields.BackwardFKRelation["CustomerLocation"]
    price_group: Union["PriceGroup", fields.ForeignKeyNullableRelation["PriceGroup"]] = fields.ForeignKeyField(
        'directories.PriceGroup', related_name='customers', on_delete=fields.RESTRICT
    )

    class Meta:
        table = "dir__customers"
        ordering = ('id',)
