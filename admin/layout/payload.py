from dataclasses import dataclass, field
from typing import Any, Protocol, TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .modal_box import ModalBox


@dataclass
class PayloadInfo:
    entity: str
    method: str
    query: dict[str, Any] = field(default_factory=dict)
    extra: Optional[dict[str, Any]] = None


class Box(Protocol):
    async def close(self):
        raise NotImplementedError

    async def add_modal(self, info: "PayloadInfo") -> "ModalBox":
        raise NotImplementedError

    async def change_title(self, title: str):
        raise NotImplementedError
