from core.repository import default_repository
from core.entities.directories import DirectoryRepository

from ..models import Position


__all__ = ["PositionRepository"]


@default_repository
class PositionRepository(DirectoryRepository):
    model = Position
