from core.repository import default_repository
from core.translations import TranslationRu, TranslationEn, Fstr
from core.entities.directories import DirectoryRepository

from ..models import PriceGroup


__all__ = ["PriceGroupRepository"]


@default_repository
class PriceGroupRepository(DirectoryRepository):
    model = PriceGroup

    _TRANSLATION_DEFAULT = _TRANSLATION_RU = TranslationRu(
        name='Ценовая группа',
        name_plural='Ценовые группы',
        fields={},
    )

    _TRANSLATION_EN = TranslationEn(
        name='Price group',
        name_plural='Price groups',
        fields={},
    )
