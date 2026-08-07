"""
MRGpt Browser

Model Mapper
"""

from __future__ import annotations

from dataclasses import fields, is_dataclass

import sqlite3


class ModelMapper:
    """
    Convert dataclass models
    to/from sqlite rows.
    """

    # -------------------------------------------------

    @staticmethod
    def to_record(model) -> dict:

        """
        Dataclass -> dict
        """

        if not is_dataclass(model):

            raise TypeError(

                f"{type(model).__name__}"

                " is not a dataclass."

            )

        record = {}

        for field in fields(model):

            record[field.name] = getattr(

                model,

                field.name

            )

        return record

    # -------------------------------------------------

    @staticmethod
    def from_record(

        model_class,

        row: sqlite3.Row,

    ):

        """
        sqlite.Row -> Model
        """

        if row is None:

            return None

        kwargs = {}

        for field in fields(model_class):

            if field.name in row.keys():

                kwargs[field.name] = row[field.name]

        return model_class(

            **kwargs

        )

    # -------------------------------------------------

    @staticmethod
    def update_model(

        model,

        row: sqlite3.Row,

    ):

        """
        Update existing model
        from sqlite.Row
        """

        if row is None:

            return model

        for field in fields(model):

            if field.name in row.keys():

                setattr(

                    model,

                    field.name,

                    row[field.name]

                )

        return model

    # -------------------------------------------------

    @staticmethod
    def copy(

        source,

        target,

    ):

        """
        Copy common fields
        between models.
        """

        source_data = ModelMapper.to_record(

            source

        )

        for key, value in source_data.items():

            if hasattr(

                target,

                key

            ):

                setattr(

                    target,

                    key,

                    value

                )

        return target