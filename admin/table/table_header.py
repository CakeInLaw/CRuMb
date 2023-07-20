from typing import TYPE_CHECKING

from flet import Row

from .cell_position import HorizontalPosition
from .table_header_cell import TableHeaderCell

if TYPE_CHECKING:
    from . import Table, TableBody


class TableHeader(Row):
    table: "Table"

    def __init__(
            self,
            cells: list[TableHeaderCell] = None,
    ):
        super().__init__(height=40, spacing=0)

        self.controls = self.cells = cells or []
        for cell in cells:
            cell.set_header(self)
        self.update_borders()

    def update_borders(self):
        length = len(self.cells)
        if length == 0:
            return
        elif length == 1:
            self.cells[0].position = HorizontalPosition.SINGLE
        else:
            self.cells[0].position = HorizontalPosition.LEFT
            for cell in self.cells[1:-1]:
                cell.position = HorizontalPosition.MIDDLE
            self.cells[-1].position = HorizontalPosition.RIGHT

    def add_cell(self, cell: TableHeaderCell, index: int = -1):
        assert index == -1 or index >= 1
        if index == -1:
            self.cells.append(cell)
        else:
            self.cells.insert(index, cell)
        cell.set_header(self)

    def set_table(self, table: "Table"):
        self.table = table

    @property
    def body(self) -> "TableBody":
        return self.table.body

    @property
    def length(self) -> int:
        return len(self.cells)
