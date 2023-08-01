from dataclasses import dataclass
from typing import Any, Optional

from flet import Container, Column, Row, IconButton, icons, ScrollMode

from core.orm import BaseModel
from core.types import BackFKData
from core.admin.components.table import Table, TableHeader, TableHeaderCell, TableBody
from .object import ObjectTableRow, ObjectTableRowWidget
from .user_input import UserInput, UserInputWidget


class TableInputWidget(UserInputWidget[list[dict[str, Any]]], Container):

    @property
    def final_value(self) -> BackFKData:
        result = []
        for widget in self.objects_list:
            if widget.initial_value is None:
                result.append(widget.final_value)
            else:
                result.append({'pk': widget.initial_value, **widget.final_value})
        return result

    def __init__(
            self,
            object_schema: ObjectTableRow,
            variant: str = 'table',
            rows_count: int = 11,
            **kwargs
    ):
        Container.__init__(self, padding=12)
        UserInputWidget.__init__(self, **kwargs)

        self.object_schema = object_schema
        self.variant = variant
        self.rows_count = rows_count
        self.objects_list: list[ObjectTableRowWidget] = [
            self.create_table_row(initial=initial)
            for initial in self.initial_value
        ]

        self.actions = Row([
            IconButton(icons.ADD_CIRCLE_OUTLINE_OUTLINED, on_click=self.handle_add_row),
            IconButton(icons.REMOVE_CIRCLE_OUTLINE_OUTLINED, on_click=self.handle_delete_row),
            IconButton(icons.ARROW_CIRCLE_UP_OUTLINED, on_click=self.handle_move_row_up),
            IconButton(icons.ARROW_CIRCLE_DOWN_OUTLINED, on_click=self.handle_move_row_down),
        ], scroll=ScrollMode.AUTO)
        self.table = self.create_table()
        self.content = Column([
            self.actions,
            self.table
        ])
        self.editable = False
        self.__finalize_init__()

    def create_table(self) -> Table:
        return Table(
            header=TableHeader(
                cells=[
                    TableHeaderCell(label=col.label, width=col.width)
                    for col in self.object_schema.fields
                ]
            ),
            body=TableBody(
                rows=self.objects_list,
                rows_count=self.rows_count
            ),
        )

    def create_table_row(self, initial: Optional[BaseModel | dict[str, Any]] = None) -> ObjectTableRowWidget:
        return self.object_schema.widget(parent=self, initial=initial)

    async def handle_add_row(self, e):
        widget = self.create_table_row()
        if self.has_ordering:
            widget.set_value({'ordering': self.table.body.length + 1})
        self.table.add_row(widget)
        self.table.body.active_row = widget
        await self.table.body.scroll_to_async(offset=-1, duration=10)

    async def handle_delete_row(self, e):
        table_body = self.table.body
        active_row: ObjectTableRowWidget = table_body.active_row  # type: ignore
        if active_row is None:
            return
        idx = active_row.index
        if idx == 0:
            if table_body.length == 1:
                table_body.active_row = None
            else:
                table_body.active_row = table_body.rows[1]
        elif idx == table_body.length - 1:
            table_body.active_row = table_body.rows[idx - 1]
        else:
            table_body.active_row = table_body.rows[idx + 1]
        table_body.rows.remove(active_row)
        if self.has_ordering:
            for i, row in enumerate(table_body.rows[idx:], start=idx + 1):
                row: ObjectTableRowWidget
                row.set_value({'ordering': i})
        await table_body.scroll_to_async(offset=-1, duration=10)

    async def handle_move_row_up(self, e):
        active_row: ObjectTableRowWidget = self.table.body.active_row  # type: ignore
        if not active_row:
            return
        idx = active_row.index
        if idx == 0:
            return
        rows = self.table.body.rows
        row_up: ObjectTableRowWidget = rows[idx - 1]  # type: ignore
        if self.has_ordering:
            active_row.set_value({'ordering': idx})
            row_up.set_value({'ordering': idx + 1})
        rows[idx], rows[idx - 1] = row_up, active_row
        await self.table.body.update_async()

    async def handle_move_row_down(self, e):
        active_row: ObjectTableRowWidget = self.table.body.active_row  # type: ignore
        if not active_row:
            return
        idx = active_row.index
        rows = self.table.body.rows
        if idx == len(rows) - 1:
            return
        row_down: ObjectTableRowWidget = rows[idx + 1]  # type: ignore
        if self.has_ordering:
            active_row.set_value({'ordering': idx + 2})
            row_down.set_value({'ordering': idx + 1})
        rows[idx], rows[idx + 1] = row_down, active_row
        await self.table.body.update_async()

    def has_changed(self) -> bool:
        return any(widget.has_changed() for widget in self.objects_list)

    def set_value(self, value: Any, initial: bool = False):
        if initial:
            return
        assert isinstance(value, dict) and all(isinstance(k, int) for k in value)
        for k, v in value.items():
            self.objects_list[k].set_value(v)

    def set_error(self, err: dict[int, dict[str, Any]]):
        for i, e in err.items():
            self.objects_list[i].set_error(e)

    def is_valid(self) -> bool:
        valid = True
        for widget in self.objects_list:
            if not widget.is_valid():
                valid = False
        return valid

    @property
    def has_ordering(self) -> bool:
        if not hasattr(self, '_cached_has_order'):
            setattr(self, '_cached_has_order', any(f.name == 'ordering' for f in self.object_schema.fields))
        return getattr(self, '_cached_has_order')


@dataclass
class TableInput(UserInput[TableInputWidget]):
    object_schema: ObjectTableRow = None
    variant: str = 'table'
    width: int = None
    height: int = None
    rows_count: int = 11

    @property
    def widget_type(self):
        return TableInputWidget

    def add_field(self, item: UserInput) -> None:
        self.object_schema.fields.append(item)

    @property
    def default_initial(self) -> list[BaseModel] | list[dict[str, Any]]:
        return []
