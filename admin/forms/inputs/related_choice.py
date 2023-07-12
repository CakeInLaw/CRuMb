from dataclasses import dataclass
from typing import Optional

from flet import TextField

from core.orm import BaseModel
from core.types import PK
from admin.forms.inputs import InputWidget, Input
from admin.exceptions import InputValidationError


class RelatedChoiceWidget(InputWidget):
    can_handle_blur: bool = False

    def __init__(self, entity: str, method: str, **kwargs):
        kwargs['validate_on_blur'] = False
        kwargs['read_only'] = True
        super().__init__(**kwargs, on_focus=self.open_choice)

        self.entity = entity
        self.method = method
        # self.on_click = self.open_choice

    @property
    def real_value(self) -> Optional[BaseModel]:
        return self._real_value

    @real_value.setter
    def real_value(self, v: Optional[BaseModel]):
        self._real_value = v
        self.value = str(v) if v else ''

    async def update_real_value(self, new_value: Optional[BaseModel]) -> None:
        self.real_value = new_value
        await self.update_async()

    @property
    def final_value(self) -> Optional[PK]:
        return self.real_value.pk if self.real_value else None

    def _set_initial_value(self, value: Optional[BaseModel]) -> None:
        self.real_value = value

    async def _validate(self) -> None:
        if self.required and self.value is None:
            raise InputValidationError('Обязательное поле')

    async def open_choice(self, e):
        await self.form.app.open_modal(
            entity=self.entity,
            method=self.method,
            current_chosen=self.real_value,
            handle_confirm=self.update_real_value,
        )


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
