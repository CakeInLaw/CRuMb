import math
from typing import TYPE_CHECKING, Type, Callable, Coroutine, Any, Optional

from flet import UserControl, Column, Text, DataTable, DataColumn, DataRow, DataCell, \
    TextSpan, TextStyle, TextDecoration, MainAxisAlignment


from core.orm import BaseModel
from core.enums import FieldTypes
from core.types import SORT, FILTERS, PK

from admin.layout import PayloadInfo
from .pagination import Pagination

if TYPE_CHECKING:
    from core.repository import Repository
    from admin.resource import Resource
    from admin.layout import BOX


class Datagrid(UserControl):

    _max_items: int = 0

    def __init__(
            self,
            box: "BOX",
            resource: "Resource",
            columns: list[str],
            sort: dict[str, bool] = None,
            filters: FILTERS = None,
            pagination_per_page: int = 25,
            pagination_count: int = 7,
            on_active_change: Callable[[DataRow], Coroutine[Any, Any, None]] = None,
            on_select: Callable[[DataRow], Coroutine[Any, Any, None]] = None,
    ):
        super().__init__()
        self.box = box
        self.resource = resource
        self.app = self.resource.app
        self.on_active_change = on_active_change
        self.on_select = on_select
        self.active = None
        self.datagrid = DataTable(
            show_checkbox_column=self.on_select is not None,
        )
        self.pagination = Pagination(
            datagrid=self,
            per_page=pagination_per_page,
            count=pagination_count
        )
        self.max_items = 0
        self.items = []
        self.columns = columns
        self.sort = sort or {}
        self.filters = filters or []

    @property
    def repository(self) -> Type["Repository"]:
        return self.resource.repository

    @property
    def selected(self) -> list[DataRow]:
        return list(filter(lambda r: r.selected, self.datagrid.rows))

    @property
    def selected_items(self) -> list["BaseModel"]:
        return list(r.item for r in filter(lambda r: r.selected, self.datagrid.rows))

    @property
    def active(self) -> Optional[DataRow]:
        return getattr(self, '_active', None)

    @active.setter
    def active(self, v: DataRow):
        if self.active:
            self.active.color = 'white'
        self._active = v
        if self.active:
            self.active.color = 'primary,0.3'

    def build(self):
        return Column([
            self.datagrid,
            self.pagination
        ], expand=True, alignment=MainAxisAlignment.SPACE_BETWEEN)

    async def update_items(self):
        self.items, self.max_items = await self.repository(
            by='admin', extra={'target': 'list'}
        ).get_all(
            skip=self.pagination.skip,
            limit=self.pagination.limit,
            sort=self.get_sort(),
            filters=self.get_filters(),
        )
        self.pagination.rebuild()

    async def update_datagrid(self):
        await self.update_items()
        await self.update_async()

    def get_filters(self) -> FILTERS:
        return self.filters

    def get_sort(self) -> SORT:
        return [name if asc else '-' + name for name, asc in self.sort.items()]

    @property
    def items(self) -> list[BaseModel]:
        return self._items

    @items.setter
    def items(self, v: list[BaseModel]):
        self._items = v
        self.fill_items()

    def open_edit_form(self, pk: PK):
        async def wrapper(e):
            await self.app.open(PayloadInfo(
                entity=self.resource.entity(),
                method='edit',
                query={'pk': pk}
            ))
        return wrapper

    def fill_items(self):
        self.datagrid.rows = rows = []
        for item in self.items:
            fields = list(self.columns.keys())
            cells = []
            if 'edit' in self.resource.methods:
                cells.append(
                    DataCell(Text(spans=[TextSpan(
                        text=self.get_value(item, fields.pop(0)),
                        style=TextStyle(color='primary', decoration=TextDecoration.UNDERLINE),
                        on_click=self.open_edit_form(item.pk)
                    )]))
                )
            for field in fields:
                cells.append(
                    DataCell(
                        Text(self.get_value(item, field)),
                        data=item.pk,
                    )
                )

            row = DataRow(cells)
            if self.use_handling_select:
                row.on_select_changed = self.handle_select
            row.item = item
            rows.append(row)
        if self.on_active_change:
            self.active = rows[0] if len(rows) > 0 else None

    @property
    def use_handling_select(self) -> bool:
        return bool(self.on_select or self.on_active_change)

    async def handle_select(self, e):
        if self.on_select:
            e.control.selected = not e.control.selected
        if self.on_active_change:
            self.active = e.control
            await self.on_active_change(self.active)
        await self.update_async()

    def get_value(self, item: BaseModel, field: str) -> str:
        field_name = self.repository.get_field_name_for_value(field)
        value = getattr(item, field_name)
        if value is None:
            return ''
        return str(value)

    @property
    def max_items(self):
        return self._max_items

    @max_items.setter
    def max_items(self, v: int):
        if self.max_items != v:
            self._max_items = v
            self.pagination.total = math.ceil(self.max_items / self.pagination.per_page)

    @property
    def columns(self) -> dict[str, DataColumn]:
        return self._columns_map

    @columns.setter
    def columns(self, v: list[str]):
        assert len(v) >= 1
        fields = self.repository.describe().all
        self._columns_map = {}
        for name in v:
            self._columns_map[name] = DataColumn(
                label=Text(self.resource.translate_field(name)),
                numeric=fields[name] in FieldTypes.numeric_types()
            )
        self.datagrid.columns = list(self._columns_map.values())
        self.fill_items()
