from dataclasses import dataclass
from typing import Optional

from flet import TextField

from .user_input import UserInputWidget, UserInput, T, _I


class InputWidget(UserInputWidget[T], TextField):
    def __init__(self, **kwargs):
        kwargs.setdefault('border', 2)
        kwargs.setdefault('border_radius', 12)
        kwargs.setdefault('text_size', 14)
        super().__init__(**kwargs)

    async def on_success_validation(self):
        if self.error_text:
            await self.set_error_text(None)

    async def set_error_text(self, text: Optional[str]):
        self.error_text = text
        await self.update_async()

    async def is_valid(self) -> bool:
        if self.error_text:
            return False
        return await super().is_valid()


@dataclass
class Input(UserInput[_I]):
    pass
