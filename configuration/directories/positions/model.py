from typing import TYPE_CHECKING

from tortoise import fields
from core.orm import fields as orm_fields

from core.entities.directories import Directory

if TYPE_CHECKING:
    from configuration.directories.models import Employee


__all__ = ["Position"]


class Position(Directory):
    id: int = orm_fields.IntField(pk=True)
    name: str = orm_fields.CharField(max_length=50)

    employees: list["Employee"] | fields.BackwardFKRelation["Employee"]

    class Meta:
        table = "dir__positions"

    def __str__(self) -> str:
        return self.name
