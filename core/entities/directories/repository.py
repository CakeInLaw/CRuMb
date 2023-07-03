from core.repository import Repository, ListValueRepository


__all__ = ["DirectoryRepository", "DirectoryValueRepository"]


class DirectoryRepository(Repository):
    pass


class DirectoryValueRepository(ListValueRepository):
    pass
