from typing import TYPE_CHECKING, Union

from tortoise import fields
from core.orm import fields as orm_fields

from ..base_nomenclature_move_documents.model import MoveDocument, MoveDocumentValuesList

if TYPE_CHECKING:
    from configuration.directories.models import Nomenclature


__all__ = ["ProductAssembly", "ProductAssemblyValuesList"]


class ProductAssembly(MoveDocument):
    """Документ сборки номенклатуры (СБ). Может быть собран по техкартам, а может и вручную"""

    PREFIX: str = 'СБ'

    product_id: int
    product: Union["Nomenclature", fields.ForeignKeyRelation["Nomenclature"]] = fields.ForeignKeyField(
        'directories.Nomenclature',
    )
    count: float = orm_fields.FloatField(min_value=0)

    values_list: list["ProductAssemblyValuesList"] | fields.BackwardFKRelation["ProductAssemblyValuesList"]

    class Meta:
        table = "doc__product_assemblies"


class ProductAssemblyValuesList(MoveDocumentValuesList):
    owner: Union["ProductAssembly", fields.ForeignKeyRelation["ProductAssembly"]] = fields.ForeignKeyField(
        'documents.ProductAssembly', related_name='values_list', on_delete=fields.CASCADE
    )

    class Meta:
        table = "doc__product_assemblies__values"
