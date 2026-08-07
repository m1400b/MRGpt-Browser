"""
MRGpt Browser

History Manager
"""

from __future__ import annotations

from datetime import datetime, timedelta

from database.repository.history_repository import (
    HistoryRepository,
)

from models.history_item import HistoryItem


class HistoryManager:

    """
    Browser History Manager
    """

    # -------------------------------------------------

    def __init__(

        self,

        repository: HistoryRepository,

    ):

        self.repository = repository

    # -------------------------------------------------

    def add_visit(

        self,

        title: str,

        url: str,

        favicon: str = "",

    ) -> HistoryItem:

        """
        Add browser visit.
        """

        item = self.repository.find_by_url(url)

        now = datetime.now().isoformat()

        # -----------------------------------------

        if item is None:

            item = HistoryItem(

                title=title,

                url=url,

                favicon=favicon,

                visit_time=now,

                visit_count=1,

                created_at=now,

                updated_at=now,

            )

            item.id = self.repository.add(item)

            return item

        # -----------------------------------------
        # Duplicate protection
        # -----------------------------------------

        try:

            last = datetime.fromisoformat(

                item.visit_time

            )

            if datetime.now() - last < timedelta(

                seconds=30

            ):

                return item

        except Exception:

            pass

        item.title = title

        item.favicon = favicon

        item.visit_time = now

        item.visit_count += 1

        item.updated_at = now

        self.repository.update(item)

        return item

    # -------------------------------------------------

    def remove(

        self,

        history_id: int,

    ):

        return self.repository.delete(

            history_id

        )

    # -------------------------------------------------

    def clear(self):

        self.repository.clear()

    # -------------------------------------------------

    def all(self):

        return self.repository.all()

    # -------------------------------------------------

    def search(

        self,

        keyword: str,

    ):

        return self.repository.search(

            keyword

        )

    # -------------------------------------------------

    def recent(

        self,

        limit: int = 50,

    ):

        return self.repository.last_visited(

            limit

        )

    # -------------------------------------------------

    def count(self):

        return self.repository.count()

    # -------------------------------------------------

    def delete_by_url(

        self,

        url: str,

    ):

        self.repository.delete_by_url(

            url

        )