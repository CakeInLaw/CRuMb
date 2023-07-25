from typing import TYPE_CHECKING, Callable, Optional, Coroutine, cast

from flet import ElevatedButton, Row, TapEvent

from core.orm import BaseModel
from admin.layout import PayloadInfo
from .base_list_form import BaseListForm, ListRecordRow

if TYPE_CHECKING:
    from admin.layout import BOX
    from .. import ModelInputForm, Primitive


class ChoiceForm(BaseListForm):

    def __init__(
            self,
            box: "BOX",
            primitive: "Primitive",
            make_choice: Callable[[Optional[BaseModel]], Coroutine[..., ..., None]],
            request_limit: int = 50,
    ):
        super().__init__(
            box=box,
            primitive=primitive,
            request_limit=request_limit
        )
        self.make_choice = make_choice

    async def on_double_click(self, e: TapEvent):
        await self.on_confirm(e)

    async def on_confirm(self, e=None):
        active_row = cast(ListRecordRow, self.table.body.active_row)
        if active_row:
            await self.make_choice(active_row.instance)
            await self.close()

    async def on_clean(self, e=None):
        await self.make_choice(None)
        await self.close()

    async def on_click_create(self, e=None):
        await self.box.add_modal(PayloadInfo(
            entity=self.resource.entity(),
            method='create',
            query={
                'on_success': self.make_choice_on_create,
            }
        ))

    async def make_choice_on_create(self, form: "ModelInputForm", instance: BaseModel):
        await self.make_choice(instance)
        await form.box.close()
        await self.close()

    def get_action_bar(self) -> Row:
        return Row([
            ElevatedButton('Выбрать', on_click=self.on_confirm),
            ElevatedButton('Очистить', on_click=self.on_clean),
            ElevatedButton('Создать', on_click=self.on_click_create),
        ])
