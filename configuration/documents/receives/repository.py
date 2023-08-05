from core.repository import register_repository, ValuesListRepository
from core.translations.langs import ru, en
from .model import Receive, ReceiveValuesList
from ..base_nomenclature_move_documents.repository import MoveDocumentRepository, NomenclatureMoveEffect

__all__ = ["ReceiveRepository", "ReceiveValuesListRepository"]


@register_repository
class ReceiveRepository(MoveDocumentRepository[Receive]):
    model = Receive
    EFFECT = NomenclatureMoveEffect.ADD

    _t_ru = ru.Entity(
        name='Поступление',
        name_plural='Поступления',
        fields={
            'provider_doc_id': 'Номер документа поставщика',
            'provider_doc_dt': 'Дата документа поставщика',
        },
    )
    _t_en = en.Entity(
        name='Receive',
        name_plural='Receives',
        fields={
            'provider_doc_id': 'Provider`s document id',
            'provider_doc_dt': 'Provider`s document date and time',
        },
    )

    async def _apply_more_side_effects(self,  records: list[ReceiveValuesList]):
        from configuration.info_registers.repositories import NomenclatureCostRepository

        records: list[ReceiveValuesList] = await self.get_values_list()
        await NomenclatureCostRepository.register(registrator=self.instance, records=[
            {
                'nomenclature_id': rec.nomenclature_id,
                'cost': rec.price,
                'count': rec.count
            }
            for rec in records
        ])

    async def cancel_side_effects(self):
        from configuration.info_registers.repositories import NomenclatureCostRepository

        await super().cancel_side_effects()
        await NomenclatureCostRepository.unregister(registrator=self.instance)


@register_repository
class ReceiveValuesListRepository(ValuesListRepository[ReceiveValuesList]):
    model = ReceiveValuesList

    _t_ru = ru.Entity(
        name='Товар',
        name_plural='Товары',
    )
    _t_en = en.Entity(
        name='Good',
        name_plural='Goods',
    )
