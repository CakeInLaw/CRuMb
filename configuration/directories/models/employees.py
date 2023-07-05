from typing import TYPE_CHECKING, Union

from tortoise import fields

from core.entities.directories import Directory

if TYPE_CHECKING:
    from configuration.directories.models import Position, User
    from configuration.documents.models import NomenclatureWriteOff


__all__ = ["Employee"]


class Employee(Directory):
    id: int = fields.IntField(pk=True)
    last_name: str = fields.CharField(max_length=40)
    first_name: str = fields.CharField(max_length=40)
    fathers_name: str = fields.CharField(max_length=40)
    position: Union["Position", fields.ForeignKeyRelation["Position"]] = fields.ForeignKeyField(
        'directories.Position', related_name='employees', on_delete=fields.RESTRICT
    )
    user: Union["User", fields.OneToOneNullableRelation["User"]] = fields.OneToOneField(
        'directories.User', related_name='employee', on_delete=fields.RESTRICT, null=True
    )

    nomenclature_write_offs_responsible_for: Union[
        list["NomenclatureWriteOff"], fields.BackwardFKRelation["NomenclatureWriteOff"]
    ]

    class Meta:
        table = "dir__employees"
        ordering = ('id',)
