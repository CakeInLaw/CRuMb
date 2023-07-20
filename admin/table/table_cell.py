from typing import TYPE_CHECKING

from flet import Container, Control, border, alignment, padding

from .cell_position import HorizontalPosition, VerticalPosition

if TYPE_CHECKING:
    from . import Table, TableHeader, TableBody, TableRow


class TableCell(Container):
    row: "TableRow"
    position: tuple[HorizontalPosition, VerticalPosition]

    def __init__(self, content: Control):
        super().__init__(
            alignment=alignment.center_left,
            padding=padding.symmetric(horizontal=5)
        )
        self.content = content

    def set_row(self, row: "TableRow"):
        self.row = row
        self.height = self.body.row_height

    @property
    def table(self) -> "Table":
        return self.row.body.table

    @property
    def header(self) -> "TableHeader":
        return self.row.body.table.header

    @property
    def body(self) -> "TableBody":
        return self.row.body
