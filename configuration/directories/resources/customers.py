from admin.resource import Resource
from ..repositories import CustomerRepository
from configuration.admin import CakeInLawAdmin
from configuration.menu_groups import Sells, Storage, Receives


@CakeInLawAdmin.register
class CustomerResource(Resource):
    repository = CustomerRepository
    datagrid_columns = ['name', 'register_address', 'price_group_id']
    present_in = (Sells,)
