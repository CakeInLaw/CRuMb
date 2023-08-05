from datetime import datetime
from typing import Optional

from tortoise import fields
from core.orm import fields as orm_fields

from core.entities.directories import Directory


__all__ = ["User"]


class User(Directory):
    id: int = orm_fields.BigIntField(pk=True)
    username: Optional[str] = orm_fields.CharField(max_length=40, unique=True, null=True)

    password_hash: str = orm_fields.CharField(max_length=100)
    password_change_dt: datetime = orm_fields.DatetimeField()

    is_superuser: bool = orm_fields.BooleanField(default=False)
    is_active: bool = orm_fields.BooleanField(default=True)
    created_at: datetime = orm_fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "dir__users"

    def __str__(self) -> str:
        return self.username
