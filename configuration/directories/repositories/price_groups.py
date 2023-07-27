from core.repository import default_repository
from core.translations import Translation
from core.entities.directories import DirectoryRepository

from ..models import PriceGroup


__all__ = ["PriceGroupRepository"]


@default_repository
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
