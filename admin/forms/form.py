from typing import TYPE_CHECKING, Optional, Any

from flet import Control, UserControl, Column, Row, Container

from core.exceptions import ObjectErrors
from .schema import FormSchema, InputGroup
from .inputs import UserInputWidget, UserInput, UndefinedValue

if TYPE_CHECKING:
    from admin.app import CRuMbAdmin
    from admin.layout import BOX


FIELDS_MAP = dict[str, UserInputWidget]


class Form(UserControl):

    schema: FormSchema = None
    fields_map: FIELDS_MAP
    action_bar: Optional[Control]
    submit_bar: Optional[Control]

    def __init__(
            self,
            app: "CRuMbAdmin",
            box: "BOX",
            *,
            initial_data: Optional[dict] = None,
    ):
        super().__init__()
        self.app = app
        self.box = box
        self.fields_map = {}
        self.initial_data = initial_data or {}

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
        return Container(Column(controls=controls))

    def build_form(self) -> Column:
        return Column(controls=self._build_form())

    def _build_form(self) -> list[Row | Column]:
        return [self._build_item(item=item) for item in self.get_form_schema()]

    def _create_widget(self, item: UserInput):
        widget = item.widget(parent=self, initial=self.initial_for(item))
        self.fields_map[item.name] = widget
        return widget

    def _build_item(self, item: UserInput | InputGroup) -> Row | Column:
        if isinstance(item, UserInput):
            return self._create_widget(item)
        controls: list[Control] = []
        item: InputGroup
        for subgroup_or_input in item:
            if isinstance(subgroup_or_input, InputGroup):
                controls.append(self._build_item(subgroup_or_input))
            elif isinstance(subgroup_or_input, UserInput):
                controls.append(self._create_widget(subgroup_or_input))
            else:
                raise ValueError('что-то пошло не так')
        return item.to_control(controls)

    def get_action_bar(self) -> Control:
        pass

    def get_submit_bar(self) -> Control:
        pass

    def get_form_schema(self) -> FormSchema:
        assert self.schema
        return self.schema

    def set_object_errors(self, err: ObjectErrors):
        _err = err.to_error()
        if '__root__' in _err:
            root = _err.pop('__root__')
            # TODO
        for field, e in _err.items():
            self.fields_map[field].set_object_error(e)

    def form_is_valid(self):
        is_valid = True
        for widget in self.fields_map.values():
            if not widget.is_valid():
                is_valid = False
        return is_valid

    @property
    def dirty_data(self):
        return {name: field.final_value for name, field in self.fields_map.items()}

    def cleaned_data(self):
        return self.dirty_data

    def initial_for(self, item: UserInput) -> Any:
        return self.initial_data.get(item.name, UndefinedValue)

    def handle_value_change(self, widget: UserInputWidget):
        pass
