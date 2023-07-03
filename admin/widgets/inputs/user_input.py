from dataclasses import dataclass
from typing import TypeVar, Optional, Any, Generic, Type, Union

from flet import Control, ControlEvent

from admin.exceptions import InputValidationError


T = TypeVar('T')
_I = TypeVar('_I', bound=Union[Control, "InputWidget"])


class UserInputWidget(Generic[T]):
    validate_on_blur: bool
    required: bool
    empty_as_none: bool

    def __init__(
            self,
            *,
            name: str = None,
            label: Optional[str] = None,
            validate_on_blur: bool = True,
            required: bool = False,
            value: T = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.name = name
        self.label = label
        self.required = required
        self.validate_on_blur = validate_on_blur
        if self.validate_on_blur:
            self.on_blur = self.validate

        self._set_initial_value(value)

    def to_value(self) -> T:
        raise NotImplementedError

    def _set_initial_value(self, value: T) -> None:
        raise NotImplementedError

    def _validate(self, v: Any) -> None:
        pass

    async def validate(self, e: ControlEvent, reraise: bool = False) -> None:
        try:
            self._validate(self.value)
            await self.on_success_validation()
        except InputValidationError as err:
            await self.set_error(err.msg)
            if reraise:
                raise err

    async def on_success_validation(self):
        pass

    async def set_error(self, msg: Optional[str]):
        self.error_text = msg
        await self.update_async()

    async def is_valid(self) -> bool:
        try:
            await self.validate(self.value, reraise=True)
        except InputValidationError:
            return False
        return True


@dataclass
class UserInput(Generic[_I]):
    name: str
    label: str
    validate_on_blur: bool = True
    required: bool = False

    def widget(self, initial: Any = None) -> _I:
        return self.widget_type(**self.__dict__, value=initial)

    @property
    def widget_type(self) -> Type[_I]:
        raise NotImplementedError
