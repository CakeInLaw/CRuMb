from core.repository import register_repository
from core.entities.directories import DirectoryRepository
from core.translations.langs import ru, en

from .model import NomenclatureCategory


__all__ = ["NomenclatureCategoryRepository"]


@register_repository
class NomenclatureCategoryRepository(DirectoryRepository):
    model = NomenclatureCategory

    _t_ru = ru.Entity(
        name='Категория номенклатуры',
        name_plural='Категории номенклатуры',
        fields={
            'type': 'Вид номенклатуры',
        },
    )
    _t_en = en.Entity(
        name='Nomenclature category',
        name_plural='Nomenclature categories',
        fields={
            'type': 'Nomenclature type',
        },
    )
