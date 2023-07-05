from typing import Optional

from flet import Control, UserControl, Column, Row

from admin.widgets.inputs.user_input import UserInputWidget, UserInput
from core.orm.base_model import BaseModel
from core.exceptions import ObjectErrors
from .schema import FormSchema, InputGroup


FIELDS_MAP = dict[str, UserInputWidget]


class Form(UserControl):

    schema: FormSchema = None
    fields_map: FIELDS_MAP
    action_bar: Optional[Control]
    submit_bar: Optional[Control]
    initial_data: Optional[BaseModel]

    def __init__(
            self,
            initial_data: Optional[BaseModel] = None
    ):
        super().__init__()
        self.fields_map = {}
        self.initial_data = initial_data

    def build(self):
        controls = []
        body = self.build_form()
        action_bar = self.get_action_bar()
        submit_bar = self.get_submit_bar()
        if action_bar:
            controls.append(action_bar)
        controls.append(body)
        if submit_bar:
            controls.append(submit_bar)
        return Column(controls=controls)

    def build_form(self) -> Column:
        return Column(controls=self._build_form())

    def _build_form(self) -> list[Row | Column]:
        return [self._build_group(group=group) for group in self.get_form_schema()]

    def _build_group(self, group: InputGroup) -> Row | Column:
        controls: list[Control] = []
        for subgroup_or_input in group:
            if isinstance(subgroup_or_input, InputGroup):
                controls.append(self._build_group(subgroup_or_input))
            elif isinstance(subgroup_or_input, UserInput):
                widget = subgroup_or_input.widget()
                self.fields_map[subgroup_or_input.name] = widget
                controls.append(widget)
        return group.to_control(controls)

    def get_action_bar(self) -> Control:
        pass

    def get_submit_bar(self) -> Control:
        pass

    def get_form_schema(self) -> FormSchema:
        assert self.schema
        return self.schema

    async def set_object_errors(self, err: ObjectErrors):
        for field, e in err.to_error().items():
            await self.fields_map[field].set_error(e['msg'])

    @property
    def dirty_data(self):
        return {name: field.final_value() for name, field in self.fields_map.items()}

    def cleaned_data(self):
        return self.dirty_data
