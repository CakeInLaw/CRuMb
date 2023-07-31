import json
from typing import TYPE_CHECKING

from flet import Container, Column, Row, Text, ElevatedButton, icons, ScrollMode, ClipBehavior


if TYPE_CHECKING:
    from core.exceptions import ObjectErrors
    from core.admin.app import CRuMbAdmin
    from core.admin.layout import Popup


class ObjectErrorsContainer(Column):
    popup: "Popup"  # пока это единственный вариант контейнера для ObjectErrorsContainer

    def __init__(
            self,
            error: "ObjectErrors",
            app: "CRuMbAdmin",
    ):
        Column.__init__(self)
        self.error = error
        self.error_text = Text(json.dumps(self.error.to_error(), ensure_ascii=False, indent=4))
        self.app = app
        self.controls = [
            Container(
                Column(
                    controls=[
                        Row(
                            controls=[self.error_text],
                            scroll=ScrollMode.AUTO,
                            width=500
                        )
                    ],
                    scroll=ScrollMode.AUTO,
                    height=500
                ),
                clip_behavior=ClipBehavior.ANTI_ALIAS_WITH_SAVE_LAYER,
                bgcolor='white',
            ),
            ElevatedButton(
                icon=icons.CONTENT_COPY_ROUNDED,
                text='Копировать в буфер',
                on_click=self.copy_error_to_clipboard
            )
        ]

    def build(self):
        return Column(
            controls=[

            ]
        )

    @classmethod
    async def open_in_popup(cls, error: "ObjectErrors", app: "CRuMbAdmin"):
        self = cls(error, app)
        popup = await app.add_popup(self, title='Ошибка валидации')
        self.popup = popup

    async def close(self):
        await self.popup.close()

    async def copy_error_to_clipboard(self, e=None):
        await self.app.page.set_clipboard_async(self.error_text.value)
