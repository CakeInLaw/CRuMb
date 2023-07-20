from typing import TYPE_CHECKING

from flet import (
    Container, Row, Stack, Text,
    GestureDetector, MouseCursor, ClipBehavior, TextOverflow, DragUpdateEvent, DragStartEvent,
    border, BorderSide,
)

from .cell_position import HorizontalPosition
from .width_changer import WidthChanger

if TYPE_CHECKING:
    from . import Table, TableHeader, TableBody


class TableHeaderCell(Container):
    header: "TableHeader"

    BORDER_SIDE = BorderSide(1, 'black')
    MIN_WIDTH = 10

    global_x_on_width_change_start: float
    width_on_width_change_start: float | int

    def __init__(
            self,
            label: str,
    ):
        super().__init__(clip_behavior=ClipBehavior.ANTI_ALIAS)
        self.position = HorizontalPosition.MIDDLE

        self.width = 150
        self.real_content = Row([Text(label, overflow=TextOverflow.ELLIPSIS)])
        self.content = Stack([self.real_content, WidthChanger(self, side='left'), WidthChanger(self, side='right')])

    def set_header(self, header: "TableHeader"):
        self.header = header

    @property
    def position(self) -> HorizontalPosition:
        return self._position

    @position.setter
    def position(self, v: HorizontalPosition):
        self._position = v
        match v:
            case HorizontalPosition.LEFT | HorizontalPosition.MIDDLE:
                self.border = border.only(right=self.BORDER_SIDE)
            case HorizontalPosition.RIGHT:
                self.border = None
            case HorizontalPosition.SINGLE:
                self.border = border.only(right=self.BORDER_SIDE, left=self.BORDER_SIDE)

    @property
    def table(self) -> "Table":
        return self.header.table

    @property
    def body(self) -> "TableBody":
        return self.header.table.body
