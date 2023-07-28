from admin.forms import Primitive
from configuration.admin import CakeInLawAdmin
from configuration.menu_groups import Nomenclature
from .default import (
    NomenclatureTypeBaseResource,
    nom_type_list_form_primitive,
    nom_type_create_form_primitive,
)
from ..repository import DishesRepository


@CakeInLawAdmin.register(
    present_in=(Nomenclature, )
)
class DishesResource(NomenclatureTypeBaseResource[DishesRepository]):
    repository = DishesRepository
    list_form_primitive = nom_type_list_form_primitive.copy().add('has_recipe')
    create_form_primitive = nom_type_create_form_primitive.copy().add(
        ('recipe', {
            'primitive': Primitive(
                ('text', {'height': 170}),
                ('ingredients', {
                    'object_schema': {
                        'primitive': Primitive(
                            ('ordering', {'width': 40}),
                            ('product_id', {'width': 300}),
                            ('count', {'width': 100})
                        )
                    }
                })
            ),
            'variant': 'column',
        })
    )
