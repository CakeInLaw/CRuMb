from typing import TypeVar

from tortoise.transactions import in_transaction

from core.repository import Repository, ListValueRepository
from .model import Document, DocumentListValue


__all__ = ["DocumentRepository", "DocumentListValueRepository"]


D = TypeVar('D', bound=Document)
DL = TypeVar('DL', bound=DocumentListValue)


class DocumentRepository(Repository[D]):

    async def conduct(self, instance: D):
        if instance.conducted:
            return
        async with in_transaction():
            await self.apply_side_effects()
            await self.edit(
                instance=instance,
                data={'conducted': True},
                run_in_transaction=False
            )

    async def unconduct(self, instance: D):
        if not instance.conducted:
            return
        async with in_transaction():
            await self.cancel_side_effects()
            await self.edit(
                instance=instance,
                data={'conducted': False},
                run_in_transaction=False
            )

    async def apply_side_effects(self):
        pass

    async def cancel_side_effects(self):
        pass


class DocumentListValueRepository(ListValueRepository[DL]):
    pass
