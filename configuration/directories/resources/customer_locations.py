from admin.forms import Primitive
from admin.resource import Resource

from ..repositories import CustomerLocationRepository
from configuration.menu_groups import Directories
from configuration.admin import CakeInLawAdmin


@CakeInLawAdmin.register(
    present_in=(Directories,)
)
class CustomerLocationResource(Resource):
    repository = CustomerLocationRepository
    list_form_primitive = Primitive('customer_id', 'name', 'delivery_address')
    form_primitive = Primitive(
        'name',
        'delivery_address',
        'customer_id'
    )

