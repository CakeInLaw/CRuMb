from typing import TYPE_CHECKING

from flet import Container, GestureDetector, Control, MouseCursor, alignment, padding

if TYPE_CHECKING:
    from . import Table, TableHeader, TableBody, TableRow


class TableCell(GestureDetector):
    row: "TableRow"

    def __init__(self, content: Control):
        GestureDetector.__init__(
            self,
            mouse_cursor=MouseCursor.CLICK,
            on_tap=self.click_handler,
        )
        self.content = self.container = Container(
            content=content,
            alignment=alignment.center_left,
            padding=padding.symmetric(horizontal=5)
        )

    def set_row(self, row: "TableRow"):
        self.row = row

    async def click_handler(self, e):
        self.activate_row()
        await self.body.update_async()

    def activate_row(self):
        self.body.active_row = self.row

    @property
    def table(self) -> "Table":
        return self.row.body.table

    @property
    def header(self) -> "TableHeader":
        return self.row.body.table.header

    @property
    def body(self) -> "TableBody":
        return self.row.body

    def change_bgcolor(self):
        row = self.row
        if row.is_active:
            self.container.bgcolor = row.ACTIVE_BGCOLOR
        elif row.is_selected:
            self.container.bgcolor = row.SELECTED_BGCOLOR
        else:
            self.container.bgcolor = row.DEFAULT_BGCOLOR
