from typing import TYPE_CHECKING, Type, Optional

from tortoise import Model
from . import fields as orm_fields

if TYPE_CHECKING:
    from core.repository import Repository


__all__ = ["BaseModel", "ListValueModel"]


class BaseModel(Model):
    BASE_PERMISSIONS: tuple[str, ...] = ('get', 'create', 'edit', 'delete')
    EXTRA_PERMISSIONS: tuple[str, ...] = ()
    IEXACT_FIELDS: tuple[str, ...] = ()

    REPOSITORIES: dict[str, Type["Repository"]]

    class Meta:
        abstract = True


class ListValueModel(BaseModel):
    """Модель для строк табличной части"""
    id: int = orm_fields.BigIntField(pk=True)
    ordering: int = orm_fields.SmallIntField(editable=True)

    class Meta:
        abstract = True
