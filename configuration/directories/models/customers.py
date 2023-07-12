from typing import TYPE_CHECKING, Union

from tortoise import fields
from core.orm import fields as orm_fields

from core.entities.directories import Directory

if TYPE_CHECKING:
    from configuration.directories.models import CustomerLocation, PriceGroup


__all__ = ["Customer"]


class Customer(Directory):
    id: int = fields.IntField(pk=True)
    name: str = orm_fields.CharField(max_length=50, unique=True)
    register_address: str = orm_fields.CharField(max_length=200)

    price_group: Union["PriceGroup", fields.ForeignKeyNullableRelation["PriceGroup"]] = fields.ForeignKeyField(
        'directories.PriceGroup', related_name='customers', on_delete=fields.RESTRICT, null=True
    )
    customer_locations: list["CustomerLocation"] | fields.BackwardFKRelation["CustomerLocation"]

    class Meta:
        table = "dir__customers"
        ordering = ('id',)

    def __str__(self) -> str:
        return self.name
