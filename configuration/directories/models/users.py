from datetime import datetime
from typing import TYPE_CHECKING, Optional

from tortoise import fields
from core.orm import fields as orm_fields

from core.entities.directories import Directory


__all__ = ["User"]


class User(Directory):
    id: int = orm_fields.BigIntField(pk=True)
    username: Optional[str] = orm_fields.CharField(max_length=40, unique=True, null=True)

    password_hash: str = orm_fields.CharField(max_length=100)
    password_change_dt: datetime = fields.DatetimeField()

    is_superuser: bool = fields.BooleanField(default=False)
    is_active: bool = fields.BooleanField(default=True)
    created_at: datetime = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "dir__users"
        ordering = ('id',)

    def __str__(self) -> str:
        return self.username
