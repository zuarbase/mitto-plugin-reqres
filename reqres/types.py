#!/usr/bin/env python3
""" Common types for Tableau Extract Job """
import enum

import typing as T

# pylint: disable=no-name-in-module
from pydantic import EmailStr
# pylint: enable=no-name-in-module

from mitto.jsoneditor import PrivateBaseModel
from mitto.script.job import schema


class StrEnum(str, enum.Enum):
    """ Enum with string values """


class Credentials(PrivateBaseModel):
    """ ReqRes user credentials """

    # EmailStr requires the `email-validator` python package
    email: EmailStr = schema(
        ...,
        """
        Email address for ReqRes account.
        """,
        title="Email address",
        examples=[
            "steve.zuar@zuar.com",
        ],
    )

    password: str = schema(
        ...,
        """
        Password for ReqRes acccount.
        """,
        # not necessary as it will be validated by ReqRes
        # just a simple example of contstraints
        min_length=1,
    )

    token: T.Optional[str] = schema(
        None,
        """
        API token.  Obtained by API call, not provided by user.
        """,
        # `hidden` prevents it from being sent to the front end
        hidden=True,
    )

    class Config:
        """ Pydantic Config """
        extra = "forbid"
