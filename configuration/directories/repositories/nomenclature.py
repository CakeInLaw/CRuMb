from core.repository import default_repository
from core.entities.directories import DirectoryRepository

from ..models import Nomenclature


__all__ = ["NomenclatureRepository"]


@default_repository
class NomenclatureRepository(DirectoryRepository):
    model = Nomenclature
