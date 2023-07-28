from configuration.admin import CakeInLawAdmin
from configuration.menu_groups import Nomenclature
from .default import (
    NomenclatureTypeBaseResource,
)
from ..repository import InventoryRepository


@CakeInLawAdmin.register(
    present_in=(Nomenclature, )
)
class InventoryResource(NomenclatureTypeBaseResource[InventoryRepository]):
    repository = InventoryRepository
