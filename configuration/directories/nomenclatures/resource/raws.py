from configuration.admin import CakeInLawAdmin
from configuration.menu_groups import Nomenclature
from .default import NomenclatureTypeBaseResource
from ..repository import RawsRepository


@CakeInLawAdmin.register(
    present_in=(Nomenclature, )
)
class RawsResource(NomenclatureTypeBaseResource[RawsRepository]):
    repository = RawsRepository

