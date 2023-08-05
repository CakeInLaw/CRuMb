from core.repository import register_repository, ValuesListRepository
from core.translations.langs import en, ru
from ..base_nomenclature_move_documents.repository import MoveDocumentRepository, NomenclatureMoveEffect
from .model import ProductAssembly, ProductAssemblyValuesList

__all__ = ["ProductAssemblyRepository", "ProductAssemblyValuesListRepository"]


@register_repository
class ProductAssemblyRepository(MoveDocumentRepository[ProductAssembly]):
    model = ProductAssembly
    EFFECT = NomenclatureMoveEffect.REDUCE

    _t_ru = ru.Entity(
        name='Возврат поставщику',
        name_plural='Возвраты поставщику',
    )
    _t_en = en.Entity(
        name='Return to provider',
        name_plural='Returns to provider',
    )

    async def _apply_more_side_effects(self, records: list[ProductAssemblyValuesList]):
        from configuration.accum_registers.repositories import NomenclatureStockRepository
        from configuration.info_registers.repositories import NomenclatureCostRepository
        await NomenclatureStockRepository.register(registrator=self.instance, records=[
            {'nomenclature_id': self.instance.product_id, 'count': self.instance.count}
        ])
        for rec in records:
            # TODO: оптимизировать
            await rec.nomenclature.fetch_related('cost')
        await NomenclatureCostRepository.register(registrator=self.instance, records=[{
            'nomenclature_id': self.instance.product_id,
            'cost': sum(rec.nomenclature.cost_value * rec.count for rec in records),
            'count': self.instance.count
        }])

    async def cancel_side_effects(self):
        await super().cancel_side_effects()
        from configuration.info_registers.repositories import NomenclatureCostRepository
        await NomenclatureCostRepository.unregister(registrator=self.instance)


@register_repository
class ProductAssemblyValuesListRepository(ValuesListRepository[ProductAssemblyValuesList]):
    model = ProductAssemblyValuesList
    related_repositories = {
        'nomenclature': 'Ingredients'
    }

    _t_ru = ru.Entity(
        name='Продукт или заготовка',
        name_plural='Продукты и заготовки',
    )
    _t_en = en.Entity(
        name='Product or provision',
        name_plural='Products and provision',
    )
