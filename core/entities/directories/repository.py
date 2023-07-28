from typing import TypeVar

from core.repository import Repository, ListValueRepository
from core.entities.directories import Directory, DirectoryListValue


__all__ = ["DirectoryRepository", "DirectoryValueRepository"]


DirectoryModel = TypeVar('DirectoryModel', bound=Directory)
DirectoryListValueModel = TypeVar('DirectoryListValueModel', bound=DirectoryListValue)


class DirectoryRepository(Repository[DirectoryModel]):
    pass


class DirectoryValueRepository(ListValueRepository[DirectoryListValueModel]):
    pass
