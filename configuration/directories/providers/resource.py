from admin.forms import Primitive
from admin.resource import Resource
from .repository import ProviderRepository
from configuration.admin import CakeInLawAdmin
from configuration.menu_groups import Directories


@CakeInLawAdmin.register(
    present_in=(Directories, )
)
class ProviderResource(Resource):
    repository = ProviderRepository
    list_form_primitive = Primitive('name')
    form_primitive = Primitive('name', 'register_address')
