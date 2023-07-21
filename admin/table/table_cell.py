from typing import TYPE_CHECKING

from flet import Container, Control, Border, BorderSide, alignment, padding

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
        self.position = (HorizontalPosition.LEFT, VerticalPosition.TOP)

    def set_row(self, row: "TableRow"):
        self.row = row
        self.border = Border()
        self.height = self.body.row_height

    @property
    def position(self) -> tuple[HorizontalPosition, VerticalPosition]:
        return self._position

    @position.setter
    def position(self, v: tuple[HorizontalPosition, VerticalPosition]):
        if getattr(self, '_position', None) == v:
            return
        self._position = v
        self.border = Border()
        if v[0] in (HorizontalPosition.LEFT, HorizontalPosition.MIDDLE):
            self.border.right = BorderSide(1, 'black')
        if v[1] in (VerticalPosition.TOP, VerticalPosition.MIDDLE):
            self.border.bottom = BorderSide(1, 'black')

    @property
    def table(self) -> "Table":
        return self.row.body.table

    @property
    def header(self) -> "TableHeader":
        return self.row.body.table.header

    @property
    def body(self) -> "TableBody":
        return self.row.body
