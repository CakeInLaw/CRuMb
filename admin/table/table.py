from flet import Container, Stack, Row, Column, OptionalNumber, ScrollMode, ClipBehavior

from .table_header import TableHeader
from .table_body import TableBody
from .table_row import TableRow


class Table(Container):
    def __init__(
            self,
            header: TableHeader,
            body: TableBody,
            height: int | float = 400,
    ):
        super().__init__(bgcolor='blue', clip_behavior=ClipBehavior.ANTI_ALIAS)
        self.header = header
        self.header.set_table(self)
        self.body = body
        self.body.set_table(self)
        self.body.height = height - self.header.height
        self.content = Row(
            controls=[Column([self.header, self.body], spacing=0)],
            scroll=ScrollMode.ALWAYS
        )

    async def update_column_width(self, index: int, width: OptionalNumber):
        self.header.cells[index].width = width
        for row in self.body.rows:
            row.cells[index].width = width
        await self.update_async()

    async def add_row(self, table_row: TableRow, index: int = -1):
        self.body.add_row(table_row=table_row, index=index)
        await self.update_async()
