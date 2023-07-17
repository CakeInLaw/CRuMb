from dataclasses import dataclass
from typing import Optional

from core.orm import BaseModel
from core.types import PK
from admin.layout import PayloadInfo
from admin.forms.inputs import InputWidget, Input
from admin.exceptions import InputValidationError


class RelatedChoiceWidget(InputWidget):

    @property
    def final_value(self) -> Optional[PK]:
        return self.real_value.pk if self.real_value else None

    @property
    def real_value(self) -> Optional[BaseModel]:
        return self._real_value

    @real_value.setter
    def real_value(self, v: Optional[BaseModel]):
        self._real_value = v
        self.value = str(v) if v else ''

    def __init__(self, entity: str, method: str, **kwargs):
        kwargs['read_only'] = True
        kwargs['on_focus'] = self.open_choice
        super().__init__(**kwargs)

        self.entity = entity
        self.method = method

    def _set_initial_value(self, value: Optional[BaseModel]) -> None:
        assert value is None or isinstance(value, BaseModel)
        self.real_value = value

    def _validate(self) -> None:
        if self.required and self.value is None:
            raise InputValidationError('Обязательное поле')

    async def update_real_value(self, new_value: Optional[BaseModel]) -> None:
        self.real_value = new_value
        await self.handle_value_change(self)

    async def open_choice(self, e):
        await self.form.box.add_modal(info=PayloadInfo(
            entity=self.entity,
            method=self.method,
            query={
                'current_chosen': self.real_value,
                'handle_confirm': self.update_real_value,
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
