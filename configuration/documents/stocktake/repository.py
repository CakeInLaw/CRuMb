from core.repository import register_repository, ValuesListRepository
from core.translations.langs import ru, en

from ..base_nomenclature_move_documents.repository import MoveDocumentRepository, NomenclatureMoveEffect
from .model import Stocktake, StocktakeValuesList

__all__ = ["StocktakeRepository", "StocktakeValuesListRepository"]


@register_repository
class StocktakeRepository(MoveDocumentRepository[Stocktake]):
    model = Stocktake
    EFFECT = NomenclatureMoveEffect.AS_IS

    _t_ru = ru.Entity(
        name='Инвентаризация',
        name_plural='Инвентаризации',
    )
    _t_en = en.Entity(
        name='Stocktake',
        name_plural='Stocktakes',
    )


@register_repository
class StocktakeValuesListRepository(ValuesListRepository[StocktakeValuesList]):
    model = StocktakeValuesList
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
