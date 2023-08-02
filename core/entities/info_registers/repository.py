from typing import TypeVar

from core.repository import Repository
from .model import InfoRegister, InfoRegisterResult


__all__ = ["InfoRegisterRepository", "InfoRegisterResultRepository"]


IR = TypeVar('IR', bound=InfoRegister)
IRR = TypeVar('IRR', bound=InfoRegisterResult)


class InfoRegisterRepository(Repository[IR]):
    pass


class InfoRegisterResultRepository(Repository[IRR]):
    pass
