from core.admin.forms import Primitive
from core.admin.resources import DocumentResource, ValuesListResource

from configuration.admin import CakeInLawAdmin
from configuration.menu_groups import Documents
from .repository import ReceiveRepository, ReceiveValuesListRepository


__all__ = ["ReceiveResource", "ReceiveValuesListResource"]


@CakeInLawAdmin.register(
    present_in=(Documents, ),
)
class ReceiveResource(DocumentResource[ReceiveRepository]):
    repository = ReceiveRepository

    list_form_primitive = Primitive(
        'unique_number',
        'dt',
        'provider_id',
        'responsible_id',
    )

    common_select_related = ('provider', 'responsible')
    edit_prefetch_related = ('values_list__nomenclature', )
    form_primitive = Primitive(
        {'name': 'group1', 'primitive': Primitive('provider_id', 'responsible_id', 'dt')},
        {'name': 'group2', 'primitive': Primitive('provider_doc_id', 'provider_doc_dt')},
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
class ReceiveValuesListResource(ValuesListResource):
    repository = ReceiveValuesListRepository
