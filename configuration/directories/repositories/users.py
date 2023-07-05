from core.repository import default_repository
from core.entities.directories import DirectoryRepository

from ..models import User


__all__ = ["UserRepository"]


@default_repository
class UserRepository(DirectoryRepository):
    model = User
