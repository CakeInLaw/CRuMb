from typing import TYPE_CHECKING

from flet import Container, Row

from core.utils import default_if_none
from .table_cell import TableCell

if TYPE_CHECKING:
    from . import Table, TableHeader, TableBody


class TableRow(Container):
    body: "TableBody"
    DEFAULT_BGCOLOR: str = '#F4F6F8'
    ACTIVE_BGCOLOR: str = '#0068FF'
    SELECTED_BGCOLOR: str = '#E9E8FF'

    def __init__(
            self,
            cells: list[TableCell] = None,
    ):
        super().__init__(bgcolor=self.DEFAULT_BGCOLOR)
        self.cells = default_if_none(cells, [])
        self.content = Row(controls=self.cells, spacing=0)
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
        self.height = self.body.row_height

    @property
    def table(self) -> "Table":
        return self.body.table

    @property
    def header(self) -> "TableHeader":
        return self.body.table.header

    @property
    def length(self) -> int:
        return len(self.cells)

    def activate(self):
        self.bgcolor = self.ACTIVE_BGCOLOR

    def deactivate(self):
        self.bgcolor = self.DEFAULT_BGCOLOR
