"""
MRGpt Browser

Base Model
"""

from __future__ import annotations

import json

from dataclasses import fields


class BaseModel:
    """
    Base class for all project models.
    """

    # ---------------------------------------------------------

    def to_dict(self) -> dict:
        """
        Convert model to dictionary.
        """

        return {

            field.name: getattr(
                self,
                field.name
            )

            for field in fields(self)

            if not field.name.startswith("_")

        }

    # ---------------------------------------------------------

    @classmethod
    def from_dict(
        cls,
        data: dict
    ):
        """
        Create model from dictionary.
        """

        valid = {

            field.name

            for field in fields(cls)

        }

        values = {

            key: value

            for key, value in data.items()

            if key in valid

        }

        return cls(**values)

    # ---------------------------------------------------------

    def to_json(
        self,
        *,
        indent: int = 4,
        ensure_ascii: bool = False
    ) -> str:
        """
        Convert model to JSON.
        """

        return json.dumps(

            self.to_dict(),

            indent=indent,

            ensure_ascii=ensure_ascii,

            default=str

        )

    # ---------------------------------------------------------

    @classmethod
    def from_json(
        cls,
        text: str
    ):
        """
        Create model from JSON.
        """

        return cls.from_dict(

            json.loads(text)

        )

    # ---------------------------------------------------------

    def copy(self):
        """
        Clone model.
        """

        return self.__class__.from_dict(

            self.to_dict()

        )

    # ---------------------------------------------------------

    def update(
        self,
        **kwargs
    ):
        """
        Update existing fields.
        """

        valid = {

            field.name

            for field in fields(self)

        }

        for key, value in kwargs.items():

            if key in valid:

                setattr(
                    self,
                    key,
                    value
                )

    # ---------------------------------------------------------

    @property
    def field_names(self):

        """
        Return model field names.
        """

        return [

            field.name

            for field in fields(self)

        ]

    # ---------------------------------------------------------

    def keys(self):

        return self.to_dict().keys()

    # ---------------------------------------------------------

    def values(self):

        return self.to_dict().values()

    # ---------------------------------------------------------

    def items(self):

        return self.to_dict().items()

    # ---------------------------------------------------------

    def __getitem__(
        self,
        key
    ):

        return getattr(
            self,
            key
        )

    # ---------------------------------------------------------

    def __setitem__(
        self,
        key,
        value
    ):

        setattr(
            self,
            key,
            value
        )

    # ---------------------------------------------------------

    def __contains__(
        self,
        key
    ):

        return key in self.field_names

    # ---------------------------------------------------------

    def __iter__(self):

        return iter(

            self.items()

        )

    # ---------------------------------------------------------

    def __len__(self):

        return len(

            self.field_names

        )

    # ---------------------------------------------------------

    def __eq__(
        self,
        other
    ):

        if not isinstance(
            other,
            self.__class__
        ):

            return False

        return (

            self.to_dict()

            ==

            other.to_dict()

        )

    # ---------------------------------------------------------

    def __repr__(self):

        values = ", ".join(

            f"{k}={v!r}"

            for k, v in self.items()

        )

        return (

            f"{self.__class__.__name__}"

            f"({values})"

        )