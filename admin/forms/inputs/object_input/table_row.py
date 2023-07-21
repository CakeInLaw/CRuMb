from dataclasses import dataclass

from admin.table import TableCell, TableRow
from .base import ObjectInputBase, ObjectInputBaseWidget


class ObjectInputTableRowWidget(ObjectInputBaseWidget, TableRow):
    children_in_table: bool = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_cells()

    def create_cells(self) -> None:
        for w in self.get_widgets():
            self.add_cell(TableCell(content=w))


@dataclass
class ObjectInputTableRow(ObjectInputBase[ObjectInputTableRowWidget]):

    @property
    def widget_type(self):
        return ObjectInputTableRowWidget
