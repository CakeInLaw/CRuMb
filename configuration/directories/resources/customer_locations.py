from admin.forms import Primitive
from admin.resource import Resource

from ..repositories import CustomerLocationRepository
from configuration.menu_groups import Sells
from configuration.admin import CakeInLawAdmin


@CakeInLawAdmin.register
class CustomerLocationResource(Resource):
    repository = CustomerLocationRepository
    datagrid_columns = ['customer', 'name', 'delivery_address']
    present_in = (Sells,)
    form_primitive = Primitive(
        'name',
        'delivery_address',
        'customer_id'
    )

