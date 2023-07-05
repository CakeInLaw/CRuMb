from typing import TYPE_CHECKING, Union

from tortoise import fields

from core.entities.directories import Directory

if TYPE_CHECKING:
    from configuration.directories.models import Customer, User


__all__ = ["CustomerLocation"]


class CustomerLocation(Directory):
    id: int = fields.IntField(pk=True)
    order: int = fields.SmallIntField()
    customer: Union["Customer", fields.ForeignKeyRelation["Customer"]] = fields.ForeignKeyField(
        'directories.Customer', related_name='customer_locations', on_delete=fields.RESTRICT
    )
    user: Union["User", fields.OneToOneRelation["User"]] = fields.OneToOneField(
        'directories.User', related_name='customer_location', on_delete=fields.RESTRICT
    )
    delivery_address: str = fields.CharField(max_length=200)

    class Meta:
        table = "dir__customer_locations"
        ordering = ('id',)
