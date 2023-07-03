from typing import Optional, Any

from flet import Control, UserControl, Column, Row

from admin.widgets.inputs.user_input import UserInputWidget, UserInput
from core.exceptions import ObjectErrors
from .schema import FormSchema, InputGroup


FIELDS_MAP = dict[str, UserInputWidget]


class Form(UserControl):

    form_schema: FormSchema = None
    fields_map: FIELDS_MAP
    action_bar: Optional[Control]
    submit_bar: Optional[Control]
    initial_data: Optional[dict[str, Any]]

    def __init__(
            self,
            action_bar: Optional[Control] = None,
            submit_bar: Optional[Control] = None,
            initial_data: dict[str, Any] = None
    ):
        super().__init__()
        self.fields_map = {}
        self.action_bar = action_bar
        self.submit_bar = submit_bar
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

    def get_action_bar(self):
        return self.action_bar

    def get_submit_bar(self):
        return self.submit_bar

    def get_form_schema(self) -> FormSchema:
        assert self.form_schema
        return self.form_schema

    async def set_object_errors(self, err: ObjectErrors):
        for field, e in err.to_error().items():
            await self.fields_map[field].set_error(e['msg'])
