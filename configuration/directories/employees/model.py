from typing import TYPE_CHECKING, Union

from tortoise import fields
from core.orm import fields as orm_fields

from core.entities.directories import Directory
from core.utils import remove_extra_spaces

if TYPE_CHECKING:
    from configuration.directories.models import Position


__all__ = ["Employee"]


class Employee(Directory):
    id: int = orm_fields.IntField(pk=True)
    last_name: str = orm_fields.CharField(max_length=40)
    first_name: str = orm_fields.CharField(max_length=40)
    fathers_name: str = orm_fields.CharField(max_length=40)
    position: Union["Position", fields.ForeignKeyRelation["Position"]] = fields.ForeignKeyField(
        'directories.Position', related_name='employees', on_delete=fields.RESTRICT
    )

    class Meta:
        table = "dir__employees"

    def __str__(self) -> str:
        return remove_extra_spaces(f'{self.last_name} {self.first_name} {self.fathers_name}')
