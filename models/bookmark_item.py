"""
MRGpt Browser

Bookmark Item Model
"""

from __future__ import annotations

from dataclasses import dataclass, field

from models.entity_model import EntityModel


@dataclass(slots=True)
class BookmarkItem(EntityModel):
    """
    Browser Bookmark
    """

    # -------------------------------------------------
    # Basic Information
    # -------------------------------------------------

    title: str = ""

    url: str = ""

    favicon: str = ""

    description: str = ""

    # -------------------------------------------------
    # Organization
    # -------------------------------------------------

    folder: str = "Bookmarks"

    position: int = 0

    tags: list[str] = field(
        default_factory=list
    )

    favorite: bool = False

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    visit_count: int = 0

    last_visit: str = ""

    # -------------------------------------------------

    @property
    def domain(self) -> str:
        """
        Website domain.
        """

        if "://" not in self.url:
            return self.url

        return self.url.split("/")[2]

    # -------------------------------------------------

    @property
    def is_empty(self) -> bool:

        return self.url == ""

    # -------------------------------------------------

    def add_tag(
        self,
        tag: str
    ):

        tag = tag.strip()

        if tag and tag not in self.tags:

            self.tags.append(tag)

    # -------------------------------------------------

    def remove_tag(
        self,
        tag: str
    ):

        if tag in self.tags:

            self.tags.remove(tag)

    # -------------------------------------------------

    def clear_tags(self):

        self.tags.clear()

    # -------------------------------------------------

    def increase_visit(self):

        self.visit_count += 1

        self.touch()

    # -------------------------------------------------

    def __str__(self):

        return f"{self.title} ({self.url})"