from typing import TypeVar

from core.admin.forms import Primitive
from core.admin.forms.widgets import EnumChoice
from core.admin.resources import DirectoryResource

from configuration.admin import CakeInLawAdmin
from ..repository import NomenclatureRepository
from ..repository.default import NomenclatureTypeBaseRepository


nom_type_list_form_primitive = Primitive('category_id', 'name', 'units', 'cost_value', 'stock_value')
nom_type_choice_form_primitive = Primitive('category_id', 'name', 'units')
nom_type_create_form_primitive = Primitive('name', 'category_id', 'units')
nom_type_edit_form_primitive = Primitive('name', 'category_id', 'units')
R = TypeVar('R', bound=NomenclatureTypeBaseRepository)
RecipeInputSchema = ('recipe', {
    'primitive': Primitive(
        ('values_list', {
            'object_schema': {
                'primitive': Primitive(
                    ('product_id', {'width': 300}),
                    ('count', {'width': 100})
                ),
            },
        }),
        'text',
    ),
})


@CakeInLawAdmin.register()
class NomenclatureResource(DirectoryResource[NomenclatureRepository]):
    repository = NomenclatureRepository

    list_form_primitive = nom_type_list_form_primitive.copy().add('type', index=0)
    choice_form_primitive = nom_type_choice_form_primitive.copy().add('type', index=0)

    common_select_related = ('category',)
    list_select_related = ('stock', 'cost')


class NomenclatureTypeBaseResource(DirectoryResource[R]):

    list_form_primitive = nom_type_list_form_primitive
    choice_form_primitive = nom_type_choice_form_primitive
    create_form_primitive = nom_type_create_form_primitive
    edit_form_primitive = nom_type_edit_form_primitive

    common_select_related = ('category',)
    list_select_related = ('stock', 'cost')
