from core.admin.forms import Primitive
from core.admin.resources import DocumentResource, ValuesListResource

from configuration.admin import CakeInLawAdmin
from configuration.menu_groups import Documents
from .repository import PriceSetupRepository, PriceSetupValuesListRepository


@CakeInLawAdmin.register(
    present_in=(Documents, )
)
class PriceSetupResource(DocumentResource[PriceSetupRepository]):
    repository = PriceSetupRepository

    list_form_primitive = Primitive(
        'unique_number',
        'dt',
        'price_group_id',
        'responsible_id',
    )

    common_select_related = ('price_group_id', 'responsible_id')
    edit_prefetch_related = ('values_list__nomenclature',)
    form_primitive = Primitive(
        {'name': 'group1', 'primitive': Primitive('price_group_id', 'responsible_id', 'dt')},
        ('values_list', {
            'object_schema': {
                'primitive': Primitive(
                    ('nomenclature_id', {'width': 300}),
                    ('price', {'width': 100}),
                ),
            },
        }),
        'comment'
    )


@CakeInLawAdmin.register()
class PriceSetupValuesListResource(ValuesListResource):
    repository = PriceSetupValuesListRepository
