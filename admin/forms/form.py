from typing import TYPE_CHECKING, Optional, Any

from flet import Control, UserControl, Column, Row, Container, padding

from core.exceptions import ObjectErrors
from .schema import FormSchema, InputGroup
from .inputs import UserInputWidget, UserInput, UndefinedValue

if TYPE_CHECKING:
    from admin.app import CRuMbAdmin


FIELDS_MAP = dict[str, UserInputWidget]


class Form(UserControl):

    schema: FormSchema = None
    fields_map: FIELDS_MAP
    action_bar: Optional[Control]
    submit_bar: Optional[Control]

    def __init__(
            self,
            app: "CRuMbAdmin",
            initial_data: Optional[dict] = None,
            lang: str = 'RU',
    ):
        super().__init__()
        self.app = app
        self.fields_map = {}
        self.initial_data = initial_data or {}
        self.LANG = lang

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
        return Container(Column(controls=controls), padding=padding.all(10))

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
                widget = subgroup_or_input.widget(form=self, initial=self.initial_for(subgroup_or_input))
                self.fields_map[subgroup_or_input.name] = widget
                controls.append(widget)
            else:
                raise ValueError('что-то пошло не так')
        return group.to_control(controls)

    def get_action_bar(self) -> Control:
        pass

    def get_submit_bar(self) -> Control:
        pass

    def get_form_schema(self) -> FormSchema:
        assert self.schema
        return self.schema

    async def set_object_errors(self, err: ObjectErrors):
        _err = err.to_error()
        if '__root__' in _err:
            root = _err.pop('__root__')
            # TODO
        for field, e in _err.items():
            await self.fields_map[field].set_object_error(e)

    async def form_is_valid(self):
        is_valid = True
        for widget in self.fields_map.values():
            if not await widget.is_valid():
                is_valid = False
        return is_valid

    @property
    def dirty_data(self):
        return {name: field.final_value for name, field in self.fields_map.items()}

    def cleaned_data(self):
        return self.dirty_data

    def initial_for(self, item: UserInput) -> Any:
        return self.initial_data.get(item.name, UndefinedValue)
