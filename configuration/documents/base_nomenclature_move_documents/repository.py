from enum import Enum
from typing import TypeVar, Literal

from core.entities.documents import DocumentRepository
from core.repository import register_repository
from core.translations.langs import ru, en
from .model import MoveDocument, MoveDocumentValuesList


__all__ = ["MoveDocumentRepository", "NomenclatureMoveEffect"]
MD = TypeVar('MD', bound=MoveDocument)
MDL = TypeVar('MDL', bound=MoveDocumentValuesList)


class NomenclatureMoveEffect(Enum):
    ADD = 'add'
    REDUCE = 'reduce'
    AS_IS = 'as_is'


class MoveDocumentRepository(DocumentRepository[MD]):
    EFFECT: NomenclatureMoveEffect

    @classmethod
    def get_stock_change_count(cls, v: float):
        if cls.EFFECT == NomenclatureMoveEffect.ADD:
            return abs(v)
        elif cls.EFFECT == NomenclatureMoveEffect.REDUCE:
            return -abs(v)
        else:
            return v

    async def apply_side_effects(self):
        from configuration.accum_registers.repositories import NomenclatureStockRepository

        records: list[MDL] = await self.get_values_list()
        await NomenclatureStockRepository.register(registrator=self.instance, records=[
            {
                'nomenclature_id': rec.nomenclature_id,
                'count': self.get_stock_change_count(rec.count)
            }
            for rec in records
        ])
        await self._apply_more_side_effects(records=records)

    # чисто для документов движения, чтобы не дергать постоянно self.get_values_list()
    async def _apply_more_side_effects(self, records: list[MDL]):
        pass

    async def cancel_side_effects(self):
        from configuration.accum_registers.repositories import NomenclatureStockRepository
        await NomenclatureStockRepository.unregister(registrator=self.instance)
