from typing import Optional

from core.repository import register_repository
from core.entities.directories import DirectoryRepository
from core.translations.langs import ru, en
from core.types import DATA

from .model import OperationReason


__all__ = ["OperationReasonRepository"]

from ...enums import OperationTypes


@register_repository
class OperationReasonRepository(DirectoryRepository):
    model = OperationReason

    _t_ru = ru.Entity(
        name='Причина операции',
        name_plural='Причины операций',
        fields={
            'operation_type': 'Вид операции'
        },
    )
    _t_en = en.Entity(
        name='Operation reason',
        name_plural='Operation reasons',
        fields={
            'operation_type': 'Operation type'
        },
    )

    async def _validate_operation_type(
            self,
            value: OperationTypes,
            data: DATA,
            instance: Optional[OperationReason]
    ) -> None:
        if instance is None:
            await self.validate_db_field('operation_type', value=value, data=data, instance=instance)
        else:
            raise ValueError('Тип операции можно установить только при создании')

