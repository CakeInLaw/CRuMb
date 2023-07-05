from typing import TYPE_CHECKING, Type, Optional

from tortoise import Model

if TYPE_CHECKING:
    from core.repository import Repository


__all__ = ["BaseModel"]


class BaseModel(Model):
    BASE_PERMISSIONS: tuple[str, ...] = ('get', 'create', 'edit', 'delete')
    EXTRA_PERMISSIONS: tuple[str, ...] = ()
    IEXACT_FIELDS: tuple[str, ...] = ()

    DEFAULT_REPOSITORY: Optional[Type["Repository"]]

    class Meta:
        abstract = True
