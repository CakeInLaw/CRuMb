from typing import TypeVar

from core.repository import Repository, ListValueRepository
from core.entities.directories import Directory, DirectoryListValue


__all__ = ["DirectoryRepository", "DirectoryListValueRepository"]


DirectoryModel = TypeVar('DirectoryModel', bound=Directory)
DirectoryListValueModel = TypeVar('DirectoryListValueModel', bound=DirectoryListValue)


class DirectoryRepository(Repository[DirectoryModel]):
    pass


class DirectoryListValueRepository(ListValueRepository[DirectoryListValueModel]):
    pass
