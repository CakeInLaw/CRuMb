from dataclasses import dataclass
from typing import Optional

from core.orm import BaseModel
from core.types import PK
from admin.layout import PayloadInfo
from admin.forms.widgets import InputWidget, Input
from admin.exceptions import InputValidationError


# TODO: переделать на dropdown с элементами, подбираемыми по вводу
class RelatedChoiceWidget(InputWidget):

    real_value: Optional[BaseModel]

    @property
    def final_value(self) -> Optional[PK]:
        return self.real_value.pk if self.real_value else None

    def __init__(self, entity: str, method: str, **kwargs):
        super().__init__(**kwargs)
        self.on_blur = None
        self.on_start_changing = self.open_choice
        self.read_only = True  # для самого видимого инпута, чтобы не изменяли текст вручную

        self.entity = entity
        self.method = method

    def set_value(self, value: Optional[BaseModel], initial: bool = False):
        assert value is None or isinstance(value, BaseModel)
        self.real_value = value
        self.value = str(self.real_value) if self.real_value else ''

    def _validate(self) -> None:
        if self.required and self.real_value is None:
            raise InputValidationError('Обязательное поле')

    async def update_real_value(self, new_value: Optional[BaseModel]) -> None:
        self.set_value(new_value)
        await self.on_end_changing.get_handler()(self)

    async def on_cancel_choice(self):
        await self.on_end_changing.get_handler()(self)

    async def open_choice(self, e):
        await self.form.box.add_modal(info=PayloadInfo(
            entity=self.entity,
            method=self.method,
            query={
                'current_chosen': self.real_value,
                'handle_confirm': self.update_real_value,
                'handle_cancel': self.on_cancel_choice,
            }
        ))


@dataclass
class RelatedChoice(Input[RelatedChoiceWidget]):
    entity: str = ''
    method: str = 'choice'

    @property
    def widget_type(self):
        return RelatedChoiceWidget

    @property
    def default_initial(self) -> Optional[BaseModel]:
        return None
