from core.admin.forms import Primitive
from core.admin.resources import DirectoryResource

from configuration.admin import CakeInLawAdmin
from configuration.menu_groups import Directories
from .repository import PriceGroupRepository


__all__ = ["PriceGroupResource"]


@CakeInLawAdmin.register(
    present_in=(Directories, )
)
class PriceGroupResource(DirectoryResource[PriceGroupRepository]):
    repository = PriceGroupRepository
    list_form_primitive = Primitive('name')
    form_primitive = Primitive('name')
