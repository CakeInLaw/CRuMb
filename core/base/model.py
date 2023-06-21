from typing import Type, Callable, Any

from tortoise import Model


__all__ = ["BaseModel", "get_field_param", "max_len_of", "default_of"]


class BaseModel(Model):
    BASE_PERMISSIONS: tuple[str, ...] = ('get', 'create', 'edit', 'delete')
    EXTRA_PERMISSIONS: tuple[str, ...] = ()

    class Meta:
        abstract = True


def get_field_param(model: Type[BaseModel], field_name: str, field_param: str):
    return getattr(model._meta.fields_map[field_name], field_param)


def max_len_of(model: Type[BaseModel]) -> Callable[[str], int]:
    return lambda field_name: get_field_param(model, field_name, 'max_length')


def default_of(model: Type[BaseModel]) -> Callable[[str], Any]:
    return lambda field_name: get_field_param(model, field_name, 'default')
