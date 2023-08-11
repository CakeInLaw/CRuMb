from core.admin.forms import Primitive
from core.admin.resources import DocumentResource, ValuesListResource

from configuration.admin import CakeInLawAdmin
from configuration.menu_groups import Documents
from .repository import ProductAssemblyRepository, ProductAssemblyValuesListRepository

__all__ = ["ProductAssemblyResource", "ProductAssemblyValuesListResource"]


@CakeInLawAdmin.register(
    present_in=(Documents, ),
)
class ProductAssemblyResource(DocumentResource[ProductAssemblyRepository]):
    repository = ProductAssemblyRepository

    list_form_primitive = Primitive(
        'unique_number',
        'dt',
        'product_id',
        'count',
        'responsible_id',
    )

    common_select_related = ('product', 'responsible')
    edit_prefetch_related = ('values_list__nomenclature', )
    form_primitive = Primitive(
        {'name': 'group1', 'primitive': Primitive('product_id', 'responsible_id', 'dt')},
        ('values_list', {
            'object_schema': {
                'primitive': Primitive(
                    ('nomenclature_id', {'width': 300}),
                    ('count', {'width': 100}),
                ),
            },
        }),
        'comment'
    )


@CakeInLawAdmin.register()
class ProductAssemblyValuesListResource(ValuesListResource):
    repository = ProductAssemblyValuesListRepository
