from core.repository import register_repository, ValuesListRepository
from core.translations.langs import ru, en
from .model import CustomerReturn, CustomerReturnValuesList
from ..base_nomenclature_move_documents.repository import MoveDocumentRepository, NomenclatureMoveEffect

__all__ = ["CustomerReturnRepository", "CustomerReturnValuesListRepository"]


@register_repository
class CustomerReturnRepository(MoveDocumentRepository[CustomerReturn]):
    model = CustomerReturn
    EFFECT = NomenclatureMoveEffect.REDUCE

    _t_ru = ru.Entity(
        name='Возврат от покупателя',
        name_plural='Возвраты от покупателя',
    )
    _t_en = en.Entity(
        name='Return from customer',
        name_plural='Returns from customer',
    )


@register_repository
class CustomerReturnValuesListRepository(ValuesListRepository[CustomerReturnValuesList]):
    model = CustomerReturnValuesList

    _t_ru = ru.Entity(
        name='Товар',
        name_plural='Товары',
    )
    _t_en = en.Entity(
        name='Good',
        name_plural='Goods',
    )
