from core.repository import ReadRepository, register_repository
from core.entities.info_registers import InfoRegisterRepository
from core.translations.langs import ru, en

from .model import NomenclaturePrice, NomenclaturePriceResult


@register_repository
class NomenclaturePriceResultRepository(ReadRepository[NomenclaturePriceResult]):
    model = NomenclaturePriceResult

    _t_ru = ru.Entity(
        name='Актуальная цена номенклатуры',
        name_plural='Актуальная цены номенклатуры',
    )
    _t_en = en.Entity(
        name='Actual price of nomenclature',
        name_plural='Actual prices of nomenclature',
    )

    def qs_select_related(self) -> tuple[str, ...]:
        return 'nomenclature', 'price_group'


@register_repository
class NomenclaturePriceRepository(InfoRegisterRepository[NomenclaturePrice, NomenclaturePriceResult]):
    model = NomenclaturePrice
    group_by = ('nomenclature_id',)
    results = NomenclaturePriceResultRepository
    main_field = 'price'

    _t_ru = ru.Entity(
        name='Цена номенклатуры',
        name_plural='Цены номенклатуры',
    )
    _t_en = en.Entity(
        name='Price of nomenclature',
        name_plural='Prices of nomenclature',
    )

    def qs_select_related(self) -> tuple[str, ...]:
        return 'nomenclature', 'price_group'
