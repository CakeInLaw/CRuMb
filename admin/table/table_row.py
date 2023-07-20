from typing import TYPE_CHECKING

from flet import Row

from core.utils import default_if_none
from .table_cell import TableCell

if TYPE_CHECKING:
    from . import Table, TableHeader, TableBody


class TableRow(Row):
    body: "TableBody"

    def __init__(
            self,
            cells: list[TableCell] = None,
    ):
        super().__init__(spacing=0)

        self.controls = self.cells = default_if_none(cells, [])
        for cell in self.cells:
            cell.row = self

    def add_cell(self, cell: TableCell, index: int = -1):
        assert index == -1 or index >= 1
        if index == -1:
            self.cells.append(cell)
        else:
            self.cells.insert(index, cell)
        cell.row = self

    def set_body(self, body: "TableBody"):
        self.body = body

    @property
    def table(self) -> "Table":
        return self.body.table

    @property
    def header(self) -> "TableHeader":
        return self.body.table.header

    @property
    def length(self) -> int:
        return len(self.cells)
