"""
MRGpt Browser

AI Message Model
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from models.entity_model import EntityModel


@dataclass(slots=True)
class AIMessage(EntityModel):
    """
    AI Conversation Message
    """

    # -------------------------------------------------
    # Session
    # -------------------------------------------------

    session_id: int = 0

    parent_id: int = 0

    # -------------------------------------------------
    # Content
    # -------------------------------------------------

    role: str = "user"

    content: str = ""

    reasoning: str = ""

    # -------------------------------------------------
    # Attachments
    # -------------------------------------------------

    images: list[str] = field(
        default_factory=list
    )

    files: list[str] = field(
        default_factory=list
    )

    # -------------------------------------------------
    # AI Information
    # -------------------------------------------------

    provider: str = ""

    model: str = ""

    finish_reason: str = ""

    # -------------------------------------------------
    # Token Usage
    # -------------------------------------------------

    prompt_tokens: int = 0

    completion_tokens: int = 0

    total_tokens: int = 0

    # -------------------------------------------------
    # Runtime
    # -------------------------------------------------

    elapsed_time: float = 0.0

    error: str = ""

    # -------------------------------------------------
    # Metadata
    # -------------------------------------------------

    favorite: bool = False

    edited: bool = False

    regenerated: bool = False

    # -------------------------------------------------

    @property
    def is_user(self):

        return self.role == "user"

    # -------------------------------------------------

    @property
    def is_assistant(self):

        return self.role == "assistant"

    # -------------------------------------------------

    @property
    def has_images(self):

        return bool(self.images)

    # -------------------------------------------------

    @property
    def has_files(self):

        return bool(self.files)

    # -------------------------------------------------

    def add_image(
        self,
        path: str
    ):

        if path not in self.images:

            self.images.append(path)

    # -------------------------------------------------

    def add_file(
        self,
        path: str
    ):

        if path not in self.files:

            self.files.append(path)

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

    def __str__(self):

        return (

            f"{self.role}: "

            f"{self.content[:40]}"

        )