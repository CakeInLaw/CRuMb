from core.repository import default_repository
from core.entities.directories import DirectoryRepository
from core.translations import Translation

from .model import Position


__all__ = ["PositionRepository"]


@default_repository
class PositionRepository(DirectoryRepository):
    model = Position

    _TRANSLATION_DEFAULT = _TRANSLATION_RU = Translation.Ru(
        name='Должность',
        name_plural='Должности',
    )

    _TRANSLATION_EN = Translation.En(
        name='Position',
        name_plural='Positions',
    )