from typing import TYPE_CHECKING, Type, Optional

from tortoise import Model, fields

if TYPE_CHECKING:
    from core.repository import Repository


__all__ = ["BaseModel", "RelatedListValueModel"]


class BaseModel(Model):
    BASE_PERMISSIONS: tuple[str, ...] = ('get', 'create', 'edit', 'delete')
    EXTRA_PERMISSIONS: tuple[str, ...] = ()
    IEXACT_FIELDS: tuple[str, ...] = ()

    DEFAULT_REPOSITORY: Optional[Type["Repository"]]

    class Meta:
        abstract = True


class RelatedListValueModel(BaseModel):
    """Модель для строк табличной части"""
    id: int = fields.BigIntField(pk=True)
    ordering: int = fields.SmallIntField()

    class Meta:
        abstract = True
