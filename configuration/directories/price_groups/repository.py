from core.repository import register_repository
from core.translations import Translation
from core.entities.directories import DirectoryRepository

from .model import PriceGroup


__all__ = ["PriceGroupRepository"]


@register_repository
class PriceGroupRepository(DirectoryRepository):
    model = PriceGroup

    _TRANSLATION_DEFAULT = _TRANSLATION_RU = Translation.Ru(
        name='Ценовая группа',
        name_plural='Ценовые группы',
    )

    _TRANSLATION_EN = Translation.En(
        name='Price group',
        name_plural='Price groups',
    )
