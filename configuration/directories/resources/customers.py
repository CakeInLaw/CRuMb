from admin.forms import Primitive
from admin.forms.widgets import Checkbox
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
        Checkbox(name='smth', label='Что-то'),
        ('customer_locations', {
            'object_schema': {
                'primitive': (
                    ('ordering', {"width": 40, 'read_only': True}),
                    ('name', {"width": 200}),
                    ('delivery_address', {"width": 220}),
                    ('user_id', {"width": 150}),
                    Checkbox(name='smth', label='Что-то')
                )
            },
        }),
    )
