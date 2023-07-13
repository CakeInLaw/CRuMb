import math
from typing import TYPE_CHECKING, Type

from flet import UserControl, Column, Text, DataTable, DataColumn, DataRow, DataCell, \
    TextSpan, TextStyle, TextDecoration, MainAxisAlignment


from core.orm import BaseModel
from core.enums import FieldTypes
from core.types import SORT, FILTERS, PK

from .pagination import Pagination

if TYPE_CHECKING:
    from admin.app import CRuMbAdmin
    from admin.resource import Resource
    from core.repository import Repository


class Datagrid(UserControl):

    _max_items: int = 0

    def __init__(
            self,
            app: "CRuMbAdmin",
            resource: "Resource",
            columns: list[str],
            sort: dict[str, bool] = None,
            filters: FILTERS = None,
            pagination_per_page: int = 25,
            pagination_count: int = 7,
    ):
        super().__init__(expand=True)
        self.app = app
        self.datagrid = DataTable(
            expand=True,
        )
        self.pagination = Pagination(
            datagrid=self,
            per_page=pagination_per_page,
            count=pagination_count
        )
        self.resource = resource
        self.max_items = 0
        self.items = []
        self.columns = columns
        self.sort = sort or {}
        self.filters = filters or []

    @property
    def repository(self) -> Type["Repository"]:
        return self.resource.repository

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
            await self.app.open(self.resource.entity(), 'edit', pk=pk)
        return wrapper

    def fill_items(self):
        self.datagrid.rows = rows = []
        for item in self.items:
            fields = list(self.columns.keys())
            cols = [
                DataCell(Text(spans=[
                    TextSpan(
                        text=self.get_value(item, fields[0]),
                        style=TextStyle(color='primary', decoration=TextDecoration.UNDERLINE),
                        on_click=self.open_edit_form(item.pk)
                    ),
                ]))
            ]
            for field in fields[1:]:
                cols.append(
                    DataCell(Text(self.get_value(item, field)), data=item.pk)
                )
            rows.append(DataRow(cols))

    def get_value(self, item: BaseModel, field: str):
        value = getattr(item, field)
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
            numeric = False
            if fields[name] in FieldTypes.numeric_types():
                numeric = True
            self._columns_map[name] = DataColumn(
                label=Text(self.resource.translate_field(name)),
                numeric=numeric
            )
        self.datagrid.columns = list(self._columns_map.values())
        self.fill_items()
