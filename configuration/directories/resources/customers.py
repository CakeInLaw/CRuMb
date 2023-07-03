from flet import Row, TextButton

from admin.forms import Form
from admin.forms.schema import FormSchema
from admin.resource import Resource
from admin.widgets.inputs import StrInput, TextInput, EnumChoice
from configuration.admin import CakeInLawAdmin
from core.exceptions import ObjectErrors
from ..repositories import CustomerRepository
from ...enums import NomenclatureTypes


class CustomerForm(Form):
    form_schema = FormSchema(
        StrInput('name', label=CustomerRepository.translate_field('name', 'RU'), max_length=50),
        EnumChoice('name', label=CustomerRepository.translate_field('name', 'RU'), enum_type=NomenclatureTypes),
        TextInput('register_address', label=CustomerRepository.translate_field('register_address', 'RU')),
    )

    def get_submit_bar(self) -> Row:
        async def create(e):
            data = {}
            all_is_valid = True
            for name, field in self.fields_map.items():
                if await field.is_valid():
                    data[name] = field.to_value()
                else:
                    all_is_valid = False
            if all_is_valid:
                try:
                    await CustomerRepository(by='admin', extra={}).create(data)
                except ObjectErrors as e:
                    await self.set_object_errors(e)
        return Row([TextButton('Создать', on_click=create)])


@CakeInLawAdmin.register()
class CustomerResource(Resource):
    repository = CustomerRepository
    datagrid_columns = ['name', 'register_address', 'price_group_id']

    def _get_form(self, *, create: bool = True) -> Form:
        return CustomerForm()
