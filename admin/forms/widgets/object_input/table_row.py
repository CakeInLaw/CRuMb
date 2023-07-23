from dataclasses import dataclass

from admin.table import TableRow
from .base import ObjectInputBase, ObjectInputBaseWidget
from ..user_input import UserInput
from ...widget_containers import TableCellWidgetContainer


class ObjectInputTableRowWidget(ObjectInputBaseWidget[TableCellWidgetContainer], TableRow):
    child_container = TableCellWidgetContainer

    def __init__(self, **kwargs):
        TableRow.__init__(self)
        ObjectInputBaseWidget.__init__(self, **kwargs)
        assert all(isinstance(f, UserInput) for f in self.fields), "Можно устанавливать только виджеты, не группы"
        self.create_cells()

    def create_cells(self) -> None:
        for w in self.get_controls():
            self.add_cell(w)

    def get_controls(self) -> list[TableCellWidgetContainer]:
        return [self._create_widget_in_container(f) for f in self.fields]


@dataclass
class ObjectInputTableRow(ObjectInputBase[ObjectInputTableRowWidget]):

    @property
    def widget_type(self):
        return ObjectInputTableRowWidget
