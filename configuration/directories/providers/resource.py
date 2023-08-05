from core.admin.forms import Primitive
from core.admin.resources import DirectoryResource

from configuration.admin import CakeInLawAdmin
from configuration.menu_groups import Directories
from .repository import ProviderRepository


@CakeInLawAdmin.register(
    present_in=(Directories, )
)
class ProviderResource(DirectoryResource[ProviderRepository]):
    repository = ProviderRepository
    list_form_primitive = Primitive('name')
    form_primitive = Primitive('name', 'register_address')
