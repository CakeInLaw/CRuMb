from core.admin.forms import Primitive
from core.admin.resources import DirectoryResource

from configuration.admin import CakeInLawAdmin
from configuration.menu_groups import Directories
from .repository import PositionRepository


__all__ = ["PositionResource"]


@CakeInLawAdmin.register(
    present_in=(Directories, )
)
class PositionResource(DirectoryResource[PositionRepository]):
    repository = PositionRepository
    list_form_primitive = Primitive('name')
    form_primitive = Primitive('name')
