from core.repository import default_repository
from core.entities.directories import DirectoryRepository
from core.translations import Translation

from ..models import OperationReason


__all__ = ["OperationReasonRepository"]


@default_repository
class OperationReasonRepository(DirectoryRepository):
    model = OperationReason

    _TRANSLATION_DEFAULT = _TRANSLATION_RU = Translation.Ru(
        name='Причина операции',
        name_plural='Причины операций',
        fields={
            'operation_type': 'Вид операции'
        },
    )
    _TRANSLATION_EN = Translation.En(
        name='Operation reason',
        name_plural='Operation reasons',
        fields={
            'operation_type': 'Operation type'
        },
    )
