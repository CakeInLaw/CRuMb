from core.repository import register_repository, ValuesListRepository
from core.translations.langs import ru, en
from .model import Sale, SaleValuesList
from ..base_nomenclature_move_documents.repository import MoveDocumentRepository, NomenclatureMoveEffect

__all__ = ["SaleRepository", "SaleValuesListRepository"]


@register_repository
class SaleRepository(MoveDocumentRepository[Sale]):
    model = Sale
    EFFECT = NomenclatureMoveEffect.REDUCE

    _t_ru = ru.Entity(
        name='Продажа',
        name_plural='Продажи',
    )
    _t_en = en.Entity(
        name='Sale',
        name_plural='Sales',
    )


@register_repository
class SaleValuesListRepository(ValuesListRepository[SaleValuesList]):
    model = SaleValuesList
    related_repositories = {
        'nomenclature': 'Sellable'
    }

    _t_ru = ru.Entity(
        name='Товар',
        name_plural='Товары',
    )
    _t_en = en.Entity(
        name='Good',
        name_plural='Goods',
    )
