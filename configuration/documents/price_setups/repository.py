from core.repository import register_repository, ValuesListRepository
from core.entities.documents import DocumentRepository
from core.translations.langs import ru, en

from .model import PriceSetup, PriceSetupValuesList

__all__ = ["PriceSetupRepository", "PriceSetupValuesListRepository"]


@register_repository
class PriceSetupRepository(DocumentRepository[PriceSetup]):
    model = PriceSetup

    _t_ru = ru.Entity(
        name='Установка цен номенклатуры',
        name_plural='Установки цен номенклатуры',
    )
    _t_en = en.Entity(
        name='Nomenclature price setup',
        name_plural='Nomenclature price setups',
    )

    async def apply_side_effects(self):
        from configuration.info_registers.repositories import NomenclaturePriceRepository
        records: list[PriceSetupValuesList] = await self.get_values_list()
        await NomenclaturePriceRepository.register(
            registrator=self.instance,
            records=[
                {
                    'nomenclature_id': rec.nomenclature_id,
                    'price_group_id': self.instance.price_group_id,
                    'price': rec.price
                }
                for rec in records
            ]
        )

    async def cancel_side_effects(self):
        from configuration.info_registers.repositories import NomenclaturePriceRepository
        await NomenclaturePriceRepository.unregister(registrator=self.instance)


@register_repository
class PriceSetupValuesListRepository(ValuesListRepository[PriceSetupValuesList]):
    model = PriceSetupValuesList
    related_repositories = {
        'nomenclature': 'Received'
    }

    _t_ru = ru.Entity(
        name='Товар',
        name_plural='Товары',
    )
    _t_en = en.Entity(
        name='Good',
        name_plural='Goods',
    )
