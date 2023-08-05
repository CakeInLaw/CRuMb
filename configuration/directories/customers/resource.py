from core.admin.forms import Primitive
from core.admin.resources import DirectoryResource

from configuration.admin import CakeInLawAdmin
from configuration.menu_groups import Directories
from .repository import CustomerRepository


__all__ = ["CustomerResource"]


@CakeInLawAdmin.register(
    present_in=(Directories, )
)
class CustomerResource(DirectoryResource[CustomerRepository]):
    repository = CustomerRepository
    list_form_primitive = Primitive('name', 'register_address', 'price_group_id')

    common_select_related = ('price_group',)
    edit_prefetch_related = ('customer_locations',)

    form_primitive = Primitive(
        'name',
        'register_address',
        'price_group_id',
    )
