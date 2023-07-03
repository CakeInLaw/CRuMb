from core.repository import default_repository
from core.entities.directories import DirectoryRepository

from ..models import OperationReason


__all__ = ["OperationReasonRepository"]


@default_repository
class OperationReasonRepository(DirectoryRepository):
    model = OperationReason
