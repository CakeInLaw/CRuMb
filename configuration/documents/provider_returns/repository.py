from core.repository import register_repository, ValuesListRepository
from core.translations.langs import en, ru
from ..base_nomenclature_move_documents.repository import MoveDocumentRepository, NomenclatureMoveEffect
from .model import ProviderReturn, ProviderReturnValuesList

__all__ = ["ProviderReturnRepository", "ProviderReturnValuesListRepository"]


@register_repository
class ProviderReturnRepository(MoveDocumentRepository[ProviderReturn]):
    model = ProviderReturn
    EFFECT = NomenclatureMoveEffect.REDUCE
    related_repositories = {
        'nomenclature': 'Received'
    }

    _t_ru = ru.Entity(
        name='Возврат поставщику',
        name_plural='Возвраты поставщику',
    )
    _t_en = en.Entity(
        name='Return to provider',
        name_plural='Returns to provider',
    )


@register_repository
class ProviderReturnValuesListRepository(ValuesListRepository[ProviderReturnValuesList]):
    model = ProviderReturnValuesList

    _t_ru = ru.Entity(
        name='Товар',
        name_plural='Товары',
    )
    _t_en = en.Entity(
        name='Good',
        name_plural='Goods',
    )
