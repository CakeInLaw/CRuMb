from core.repository import default_repository
from core.entities.directories import DirectoryRepository

from ..models import Provider


__all__ = ["ProviderRepository"]


@default_repository
class ProviderRepository(DirectoryRepository):
    model = Provider
