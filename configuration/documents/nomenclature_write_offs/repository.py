from core.repository import register_repository, ValuesListRepository
from core.translations.langs import ru, en
from .model import NomenclatureWriteOff, NomenclatureWriteOffValuesList
from ..base_nomenclature_move_documents.repository import MoveDocumentRepository, NomenclatureMoveEffect

__all__ = ["NomenclatureWriteOffRepository", "NomenclatureWriteOffValuesListRepository"]


@register_repository
class NomenclatureWriteOffRepository(MoveDocumentRepository[NomenclatureWriteOff]):
    model = NomenclatureWriteOff
    EFFECT = NomenclatureMoveEffect.REDUCE

    _t_ru = ru.Entity(
        name='Списание номенклатуры',
        name_plural='Списания номенклатуры',
    )
    _t_en = en.Entity(
        name='Nomenclature write off',
        name_plural='Nomenclature write offs',
    )


@register_repository
class NomenclatureWriteOffValuesListRepository(ValuesListRepository[NomenclatureWriteOffValuesList]):
    model = NomenclatureWriteOffValuesList
    related_repositories = {
        'nomenclature': '__default__'
    }

    _t_ru = ru.Entity(
        name='Товар',
        name_plural='Товары',
    )
    _t_en = en.Entity(
        name='Good',
        name_plural='Goods',
    )
