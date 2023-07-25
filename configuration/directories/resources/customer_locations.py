from admin.forms import Primitive
from admin.resource import Resource

from ..repositories import CustomerLocationRepository
from configuration.menu_groups import Sells
from configuration.admin import CakeInLawAdmin


@CakeInLawAdmin.register(
    present_in=(Sells,)
)
class CustomerLocationResource(Resource):
    repository = CustomerLocationRepository
    list_primitive = Primitive('customer_id', 'name', 'delivery_address')
    form_primitive = Primitive(
        'name',
        'delivery_address',
        'customer_id'
    )

