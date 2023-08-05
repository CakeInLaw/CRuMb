from core.repository import ReadRepository, register_repository
from core.entities.info_registers import InfoRegisterRepository
from core.translations.langs import ru, en

from .model import NomenclatureCost, NomenclatureCostResult


@register_repository
class NomenclatureCostResultRepository(ReadRepository[NomenclatureCostResult]):
    model = NomenclatureCostResult

    _t_ru = ru.Entity(
        name='Актуальная себестоимость номенклатуры',
        name_plural='Актуальная себестоимость номенклатуры',
    )
    _t_en = en.Entity(
        name='Actual cost of nomenclature',
        name_plural='Actual cost of nomenclature',
    )

    def qs_select_related(self) -> tuple[str]:
        return ('nomenclature',)


@register_repository
class NomenclatureCostRepository(InfoRegisterRepository[NomenclatureCost, NomenclatureCostResult]):
    model = NomenclatureCost
    group_by = ('nomenclature_id',)
    results = NomenclatureCostResultRepository
    main_field = 'cost'
    side_fields = ('count',)

    _t_ru = ru.Entity(
        name='Себестимость номенклатуры',
        name_plural='Себестимость номенклатуры',
    )
    _t_en = en.Entity(
        name='Cost of nomenclature',
        name_plural='Cost of nomenclature',
    )

    def qs_select_related(self) -> tuple[str]:
        return ('nomenclature',)
