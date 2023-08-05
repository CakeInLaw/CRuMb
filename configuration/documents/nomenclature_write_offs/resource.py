from core.admin.forms import Primitive
from core.admin.resources import DocumentResource, ValuesListResource

from configuration.admin import CakeInLawAdmin
from configuration.menu_groups import Documents
from .repository import NomenclatureWriteOffRepository, NomenclatureWriteOffValuesListRepository

__all__ = ["NomenclatureWriteOffResource", "NomenclatureWriteOffValuesListResource"]


@CakeInLawAdmin.register(
    present_in=(Documents, ),
)
class NomenclatureWriteOffResource(DocumentResource[NomenclatureWriteOffRepository]):
    repository = NomenclatureWriteOffRepository

    list_form_primitive = Primitive(
        'unique_number',
        'dt',
        'responsible_id',
        'reason_id',
    )

    common_select_related = ('responsible',)
    edit_prefetch_related = ('values_list__nomenclature', )
    form_primitive = Primitive(
        {'name': 'group1', 'primitive': Primitive('reason_id', 'responsible_id', 'dt')},
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
class NomenclatureWriteOffValuesListResource(ValuesListResource):
    repository = NomenclatureWriteOffValuesListRepository
