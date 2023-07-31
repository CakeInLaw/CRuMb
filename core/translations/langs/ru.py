from dataclasses import dataclass

from ..entity import EntityTranslation
from ..interface import InterfaceTranslation


__all__ = ["interface", "Entity"]


interface = InterfaceTranslation(
    __lang__='Русский',
    settings='Настройки',
    sign_in='Авторизоваться',
    sign_out='Выйти',
    common_fields={
        'name': 'Наименование',
        'ordering': '№',
        'count': 'Количество',
    }
)


@dataclass
class Entity(EntityTranslation):
    _choice: str = 'Выбор'
    _creation: str = 'Создание'
