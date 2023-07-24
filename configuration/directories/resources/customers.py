from flet import TextButton

from admin.forms import Primitive, ModelForm
from admin.layout import PayloadInfo
from admin.resource import Resource
from ..repositories import CustomerRepository
from configuration.admin import CakeInLawAdmin
from configuration.menu_groups import Sells


class CreateCustomerForm(ModelForm):
    async def did_mount_async(self):
        async def open_in_modal(e):
            await self.box.add_modal(PayloadInfo(
                entity=self.resource.entity(),
                method='create',
            ))

        self.action_bar.controls.append(TextButton('Открыть в модалке', on_click=open_in_modal))
        await self.update_async()


@CakeInLawAdmin.register(
    present_in=(Sells, )
)
class CustomerResource(Resource):
    repository = CustomerRepository
    datagrid_columns = ['name', 'register_address', 'price_group_id']

    create_model_form = CreateCustomerForm
    form_primitive = Primitive(
        'name',
        'register_address',
        'price_group_id',
        ('customer_locations', {
            'object_schema': {
                'primitive': (
                    ('ordering', {"width": 40}),
                    ('name', {"width": 200}),
                    ('delivery_address', {"width": 220}),
                    ('user_id', {"width": 150})
                )
            },
        })
    )
