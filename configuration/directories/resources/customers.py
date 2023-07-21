from admin.forms import Primitive, inputs
from admin.resource import Resource
from ..repositories import CustomerRepository
from configuration.admin import CakeInLawAdmin
from configuration.menu_groups import Sells


@CakeInLawAdmin.register(
    present_in=(Sells, )
)
class CustomerResource(Resource):
    repository = CustomerRepository
    datagrid_columns = ['name', 'register_address', 'price_group_id']

    form_primitive = Primitive(
        'name',
        'register_address',
        'price_group_id',
        ('customer_locations', {
            'object_schema': {
                'primitive': (
                    ('ordering', {"default_width": 40}),
                    ('name', {"default_width": 200}),
                    ('delivery_address', {"default_width": 220}),
                    ('user_id', {"default_width": 150})
                )
            }
        })
    )
