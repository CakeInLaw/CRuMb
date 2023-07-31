from core.repository import register_repository
from core.translations.langs import ru, en
from core.entities.directories import DirectoryRepository

from .model import PriceGroup


__all__ = ["PriceGroupRepository"]


@register_repository
class PriceGroupRepository(DirectoryRepository):
    model = PriceGroup

    _t_ru = ru.Entity(
        name='Ценовая группа',
        name_plural='Ценовые группы',
    )

    _t_en = en.Entity(
        name='Price group',
        name_plural='Price groups',
    )
