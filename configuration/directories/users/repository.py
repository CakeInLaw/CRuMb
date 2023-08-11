from core.repository import register_repository
from core.users.repository import BaseUserRepository
from core.users.translations import RuUserEntityTranslation, EnUserEntityTranslation

from .model import User


__all__ = ["UserRepository"]


@register_repository
class UserRepository(BaseUserRepository[User]):
    model = User

    _t_ru = RuUserEntityTranslation()

    _t_en = EnUserEntityTranslation()
