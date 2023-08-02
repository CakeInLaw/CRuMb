from typing import TypeVar, Any, TYPE_CHECKING

from core.repository import Repository
from .model import AccumRegister, AccumRegisterResult

if TYPE_CHECKING:
    from core.entities.documents import Document


__all__ = ["AccumRegisterRepository", "AccumRegisterResultRepository"]


AR = TypeVar('AR', bound=AccumRegister)
ARR = TypeVar('ARR', bound=AccumRegisterResult)


class AccumRegisterRepository(Repository[AR]):
    HAS_CREATE = False
    HAS_EDIT = False
    HAS_DELETE_ONE = False
    HAS_DELETE_MANY = False

    async def register_records(
            self,
            registrator: "Document",
            records: list[dict[str, Any]],
    ):
        reg_number = registrator.unique_number
        reg_dt = registrator.dt
        instances: list[AR] = []
        for rec in records:
            instances.append(self.model(
                registrator=reg_number,
                dt=reg_dt,
                **rec
            ))
        instances = await self.model.bulk_create(instances, batch_size=100)
        await self.recalc_results(instances)

    async def recalc_results(self, records: list[AR]):
        raise NotImplementedError


class AccumRegisterResultRepository(Repository[ARR]):
    HAS_DELETE_ONE = False
    HAS_DELETE_MANY = False
