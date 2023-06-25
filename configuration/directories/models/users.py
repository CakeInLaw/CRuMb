from datetime import datetime
from typing import TYPE_CHECKING, Optional, Union

from tortoise import fields

from core.entities.directories.model import Directory

if TYPE_CHECKING:
    from configuration.directories.models import Employee, CustomerLocation


__all__ = ["User"]


class User(Directory):
    id: int = fields.BigIntField(pk=True)
    username: Optional[str] = fields.CharField(max_length=40, unique=True, null=True)

    password_hash: str = fields.CharField(max_length=200)
    password_change_dt: datetime = fields.DatetimeField()
    password_salt: str = fields.CharField(max_length=50)

    is_superuser: bool = fields.BooleanField(default=False)
    is_active: bool = fields.BooleanField(default=True)
    created_at: datetime = fields.DatetimeField(auto_now_add=True)

    employee: Union["Employee", fields.BackwardOneToOneRelation["Employee"]]
    customer_location: Union["CustomerLocation", fields.BackwardOneToOneRelation["CustomerLocation"]]

    class Meta:
        table = "dir__users"
        ordering = ('id',)
