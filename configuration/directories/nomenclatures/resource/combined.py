from typing import TypeVar

from core.admin.resources import DirectoryResource
from configuration.admin import CakeInLawAdmin
from .default import nom_type_list_form_primitive, nom_type_choice_form_primitive
from ..repository.combined import CombinedNomenclatureTypeRepository
from ..repository import IngredientRepository, AssembledRepository, ReceivedRepository, SellableRepository


REP = TypeVar('REP', bound=CombinedNomenclatureTypeRepository)


class CombinedNomenclatureTypeResource(DirectoryResource[REP]):
    list_form_primitive = nom_type_list_form_primitive.copy().add('type', index=0)
    choice_form_primitive = nom_type_choice_form_primitive.copy().add('type', index=0)
    common_select_related = ('category', )


@CakeInLawAdmin.register()
class IngredientResource(CombinedNomenclatureTypeResource[IngredientRepository]):
    repository = IngredientRepository


@CakeInLawAdmin.register()
class AssembledResource(CombinedNomenclatureTypeResource[AssembledRepository]):
    repository = AssembledRepository


@CakeInLawAdmin.register()
class ReceivedResource(CombinedNomenclatureTypeResource[ReceivedRepository]):
    repository = ReceivedRepository


@CakeInLawAdmin.register()
class SellableResource(CombinedNomenclatureTypeResource[SellableRepository]):
    repository = SellableRepository
