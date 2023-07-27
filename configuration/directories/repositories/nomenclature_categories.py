from core.repository import default_repository
from core.entities.directories import DirectoryRepository
from core.translations import Translation

from ..models import NomenclatureCategory


__all__ = ["NomenclatureCategoryRepository"]


@default_repository
class NomenclatureCategoryRepository(DirectoryRepository):
    model = NomenclatureCategory

    _TRANSLATION_DEFAULT = _TRANSLATION_RU = Translation.Ru(
        name='Категория номенклатуры',
        name_plural='Категории номенклатуры',
        fields={
            'type': 'Вид номенклатуры',
        },
    )
    _TRANSLATION_EN = Translation.En(
        name='Nomenclature category',
        name_plural='Nomenclature categories',
        fields={
            'type': 'Nomenclature type',
        },
    )
