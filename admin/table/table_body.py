from typing import TYPE_CHECKING

from flet import ListView as FletListView

from core.utils import default_if_none
from .cell_position import VerticalPosition
from .table_row import TableRow

if TYPE_CHECKING:
    from . import Table, TableHeader


class TableBody(FletListView):
    table: "Table"
    rows: list[TableRow]
    row_height = 30

    def __init__(
            self,
            rows: list[TableRow] = None,
            rows_count: int = 12,
    ):
        super().__init__(
            item_extent=self.row_height,
            height=self.row_height * rows_count,
            spacing=0,
        )
        self.rows = default_if_none(rows, [])
        self.controls = self.rows
        self.update_borders()

    def set_table(self, table: "Table"):
        self.table = table

        header_length = self.header.length
        assert all(row.length == header_length for row in self.rows)
        for row in self.rows:
            row.set_body(self)
        for i, hc in enumerate(self.header.cells):
            w = hc.width
            for row in self.rows:
                row.cells[i].width = w
        self.update_width()

    def update_width(self):
        self.width = sum([c.width for c in self.header.cells])

    def update_borders(self):
        length = len(self.rows)
        if length == 0:
            return
        elif length == 1:
            self.rows[0].update_borders(VerticalPosition.SINGLE)
        else:
            self.rows[0].update_borders(VerticalPosition.TOP)
            for cell in self.rows[1:-1]:
                cell.update_borders(VerticalPosition.MIDDLE)
            self.rows[-1].update_borders(VerticalPosition.BOTTOM)

    def add_row(self, table_row: TableRow, index: int = -1):
        assert index == -1 or index >= 1
        assert table_row.length == self.header.length
        if index == -1:
            self.rows.append(table_row)
        else:
            self.rows.insert(index, table_row)
        for i, hc in enumerate(self.header.cells):
            table_row.cells[i].width = hc.width
        table_row.set_body(self)
        self.update_borders()

    @property
    def length(self) -> int:
        return len(self.rows)

    @property
    def header(self) -> "TableHeader":
        return self.table.header
