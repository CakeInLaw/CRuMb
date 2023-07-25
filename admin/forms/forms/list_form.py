from flet import Row, ElevatedButton, TapEvent

from admin.layout import PayloadInfo
from .base_list_form import BaseListForm, ListRecordRow


class ListForm(BaseListForm):
    async def on_double_click(self, e: TapEvent):
        row: ListRecordRow = e.control.row
        await self.app.open(PayloadInfo(
            entity=self.resource.entity(),
            method='edit',
            query={
                'pk': row.instance.pk
            }
        ))

    def get_action_bar(self) -> Row:
        return Row([
            ElevatedButton('Создать', on_click=self.open_create_form)
        ])

    async def open_create_form(self, e=None):
        await self.app.open(PayloadInfo(
            entity=self.resource.entity(),
            method='create',
        ))
