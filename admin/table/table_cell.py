from typing import TYPE_CHECKING

from flet import Container, Control, alignment, padding

if TYPE_CHECKING:
    from . import Table, TableHeader, TableBody, TableRow


class TableCell(Container):
    row: "TableRow"

    def __init__(self, content: Control):
        super().__init__(
            alignment=alignment.center_left,
            padding=padding.symmetric(horizontal=5)
        )
        self.content = content

    def set_row(self, row: "TableRow"):
        self.row = row

    @property
    def table(self) -> "Table":
        return self.row.body.table

    @property
    def header(self) -> "TableHeader":
        return self.row.body.table.header

    @property
    def body(self) -> "TableBody":
        return self.row.body
