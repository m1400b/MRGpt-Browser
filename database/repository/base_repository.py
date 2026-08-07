"""
MRGpt Browser

Base Repository
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, Iterable, TypeVar

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    """
    Base Repository Interface

    تمام Repositoryهای پروژه از این کلاس
    ارث‌بری می‌کنند.
    """

    # -------------------------------------------------

    @abstractmethod
    def add(self, item: T) -> int:
        """
        Insert new item.

        Returns:
            Row ID
        """
        raise NotImplementedError

    # -------------------------------------------------

    @abstractmethod
    def update(self, item: T) -> bool:
        """
        Update existing item.
        """
        raise NotImplementedError

    # -------------------------------------------------

    @abstractmethod
    def delete(self, item_id: int) -> bool:
        """
        Delete item by ID.
        """
        raise NotImplementedError

    # -------------------------------------------------

    @abstractmethod
    def get(self, item_id: int) -> T | None:
        """
        Get item by ID.
        """
        raise NotImplementedError

    # -------------------------------------------------

    @abstractmethod
    def all(self) -> list[T]:
        """
        Get all items.
        """
        raise NotImplementedError

    # -------------------------------------------------

    @abstractmethod
    def count(self) -> int:
        """
        Number of stored items.
        """
        raise NotImplementedError

    # -------------------------------------------------

    @abstractmethod
    def exists(self, item_id: int) -> bool:
        """
        Check item existence.
        """
        raise NotImplementedError

    # -------------------------------------------------

    @abstractmethod
    def clear(self) -> None:
        """
        Delete all records.
        """
        raise NotImplementedError

    # -------------------------------------------------

    def add_many(
        self,
        items: Iterable[T]
    ) -> list[int]:
        """
        Insert multiple items.
        """

        ids: list[int] = []

        for item in items:

            ids.append(

                self.add(item)

            )

        return ids

    # -------------------------------------------------

    def delete_many(
        self,
        ids: Iterable[int]
    ) -> int:
        """
        Delete multiple items.

        Returns:
            Number of deleted items.
        """

        deleted = 0

        for item_id in ids:

            if self.delete(item_id):

                deleted += 1

        return deleted

    # -------------------------------------------------

    def is_empty(self) -> bool:
        """
        Repository has no records.
        """

        return self.count() == 0