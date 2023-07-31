from dataclasses import dataclass, field
from typing import Any, Protocol, TYPE_CHECKING, Optional, Callable, Coroutine

if TYPE_CHECKING:
    from .modal_box import ModalBox


@dataclass
class PayloadInfo:
    entity: str
    method: str
    query: dict[str, Any] = field(default_factory=dict)
    extra: Optional[dict[str, Any]] = None


class Box(Protocol):
    on_close: Callable[[], Coroutine[..., ..., None]]

    async def close(self):
        raise NotImplementedError

    async def add_modal(self, info: "PayloadInfo") -> "ModalBox":
        raise NotImplementedError

    def change_title(self, title: str):
        raise NotImplementedError

    @staticmethod
    def filter_payload_query(info: PayloadInfo):
        """убирает из query ключи, которые предназначены для Box"""
        return {k: v for k, v in info.query.items() if not k.startswith('BOX_')}
