from typing import TYPE_CHECKING

from tortoise import fields
from core.directories.model import Directory

if TYPE_CHECKING:
    from configuration.directories.models import Employee


__all__ = ["Position"]


class Position(Directory):
    id: int = fields.IntField(pk=True)
    name: str = fields.CharField(max_length=50)

    employees: list["Employee"] | fields.BackwardFKRelation["Employee"]

    class Meta:
        table = "dir__positions"
        ordering = ('id',)
