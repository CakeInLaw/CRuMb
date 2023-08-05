from core.repository import ReadRepository, register_repository
from core.entities.accum_registers import AccumRegisterRepository
from core.translations.langs import ru, en

from .model import NomenclatureStock, NomenclatureStockResult


@register_repository
class NomenclatureStockResultRepository(ReadRepository[NomenclatureStockResult]):
    model = NomenclatureStockResult

    _t_ru = ru.Entity(
        name='Актуальный остаток номенклатуры',
        name_plural='Актуальные остатки номенклатуры',
    )
    _t_en = en.Entity(
        name='Actual stock of nomenclature',
        name_plural='Actual stock of nomenclature',
    )

    def qs_select_related(self) -> tuple[str]:
        return ('nomenclature',)


@register_repository
class NomenclatureStockRepository(AccumRegisterRepository[NomenclatureStock, NomenclatureStockResult]):
    model = NomenclatureStock
    group_by = ('nomenclature_id',)
    results = NomenclatureStockResultRepository

    _t_ru = ru.Entity(
        name='Остаток номенклатуры',
        name_plural='Остатки номенклатуры',
    )
    _t_en = en.Entity(
        name='Stock of nomenclature',
        name_plural='Stock of nomenclature',
    )

    def qs_select_related(self) -> tuple[str]:
        return ('nomenclature',)
