from core.admin.forms import Primitive
from core.admin.resources import DocumentResource, ValuesListResource

from configuration.admin import CakeInLawAdmin
from configuration.menu_groups import Documents
from .repository import CustomerReturnRepository, CustomerReturnValuesListRepository

__all__ = ["CustomerReturnResource", "CustomerReturnValuesListResource"]


@CakeInLawAdmin.register(
    present_in=(Documents, ),
)
class CustomerReturnResource(DocumentResource[CustomerReturnRepository]):
    repository = CustomerReturnRepository

    list_form_primitive = Primitive(
        'unique_number',
        'dt',
        'sale_id',
        'responsible_id',
    )

    common_select_related = ('sale', 'responsible')
    edit_prefetch_related = ('values_list__nomenclature', )
    form_primitive = Primitive(
        {'name': 'group1', 'primitive': Primitive('sale_id', 'responsible_id', 'dt')},
        ('values_list', {
            'object_schema': {
                'primitive': Primitive(
                    ('nomenclature_id', {'width': 300}),
                    ('count', {'width': 100}),
                    ('price', {'width': 100}),
                ),
            },
        }),
        'comment'
    )


@CakeInLawAdmin.register()
class CustomerReturnValuesListResource(ValuesListResource):
    repository = CustomerReturnValuesListRepository
