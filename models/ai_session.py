"""
MRGpt Browser

AI Session Model
"""

from __future__ import annotations

from dataclasses import dataclass, field

from models.entity_model import EntityModel


@dataclass(slots=True)
class AISession(EntityModel):
    """
    AI Conversation Session
    """

    # -------------------------------------------------
    # General
    # -------------------------------------------------

    title: str = "New Chat"

    provider: str = ""

    model: str = ""

    system_prompt: str = ""

    # -------------------------------------------------
    # Parameters
    # -------------------------------------------------

    temperature: float = 0.7

    max_tokens: int = 4096

    top_p: float = 1.0

    frequency_penalty: float = 0.0

    presence_penalty: float = 0.0

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    message_count: int = 0

    prompt_tokens: int = 0

    completion_tokens: int = 0

    total_tokens: int = 0

    # -------------------------------------------------
    # State
    # -------------------------------------------------

    favorite: bool = False

    archived: bool = False

    pinned: bool = False

    # -------------------------------------------------
    # Metadata
    # -------------------------------------------------

    tags: list[str] = field(
        default_factory=list
    )

    description: str = ""

    # -------------------------------------------------

    @property
    def is_empty(self) -> bool:

        return self.message_count == 0

    # -------------------------------------------------

    def add_message(self):

        self.message_count += 1

        self.touch()

    # -------------------------------------------------

    def add_tokens(
        self,
        prompt: int,
        completion: int
    ):

        self.prompt_tokens += prompt

        self.completion_tokens += completion

        self.total_tokens = (

            self.prompt_tokens

            +

            self.completion_tokens

        )

        self.touch()

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

    def __str__(self):

        return (

            f"{self.title} "

            f"[{self.provider}]"

        )