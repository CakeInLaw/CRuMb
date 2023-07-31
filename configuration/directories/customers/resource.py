from core.admin.forms import Primitive
from core.admin.resource import Resource

from configuration.admin import CakeInLawAdmin
from configuration.menu_groups import Directories
from .repository import CustomerRepository


__all__ = ["CustomerResource"]


@CakeInLawAdmin.register(
    present_in=(Directories, )
)
class CustomerResource(Resource):
    repository = CustomerRepository
    datagrid_columns = ['name', 'register_address', 'price_group_id']
    list_form_primitive = Primitive('name', 'register_address', 'price_group_id')

    form_primitive = Primitive(
        'name',
        'register_address',
        'price_group_id',
        ('customer_locations', {
            'object_schema': {
                'primitive': Primitive(
                    ('ordering', {"width": 40}),
                    ('name', {"width": 200}),
                    ('delivery_address', {"width": 220}),
                )
            },
        }),
    )
