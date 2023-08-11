from core.users.resource import BaseUserResource

from configuration.admin import CakeInLawAdmin
from configuration.menu_groups import Directories
from .repository import UserRepository

__all__ = ["UserResource"]


@CakeInLawAdmin.register(
    present_in=(Directories,)
)
class UserResource(BaseUserResource[UserRepository]):
    repository = UserRepository
