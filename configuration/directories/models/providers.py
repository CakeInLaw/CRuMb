from typing import TYPE_CHECKING

from tortoise import fields

from core.entities.directories import Directory

if TYPE_CHECKING:
    from configuration.documents.models import Receive


__all__ = ["Provider"]


class Provider(Directory):
    id: int = fields.IntField(pk=True)
    name: str = fields.CharField(max_length=50)
    register_address: str = fields.CharField(max_length=200)

    receives: list["Receive"] | fields.BackwardFKRelation["Receive"]

    class Meta:
        table = "dir__providers"
        ordering = ('id',)
