from .repository import Repository
from ..types import LIST_VALUE_MODEL, PK


class ListValueRepository(Repository[LIST_VALUE_MODEL]):
    async def _delete_many(self, item_pk_list: list[PK]) -> int:
        return await self._get_many_queryset(item_pk_list).delete()

    async def _delete_one(self, instance: LIST_VALUE_MODEL) -> None:
        await instance.delete()
