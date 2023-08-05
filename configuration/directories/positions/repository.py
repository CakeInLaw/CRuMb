from core.repository import register_repository
from core.entities.directories import DirectoryRepository
from core.translations.langs import ru, en

from .model import Position


__all__ = ["PositionRepository"]


@register_repository
class PositionRepository(DirectoryRepository[Position]):
    model = Position

    _t_ru = ru.Entity(
        name='Должность',
        name_plural='Должности',
    )

    _t_en = en.Entity(
        name='Position',
        name_plural='Positions',
    )
