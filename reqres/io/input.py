"""
ReqRes Inputter

By convention, a plugin's inputter is located in
`<plugin-name>/<plugin-name>/iov2/input.py`; it is typically named `Input`.
Some plugins have more than one iputter.

``Input`` is a Pydantic class.  Documentation describing ``Input`` is
automatically created using ``sphinx-jsonschema`` if an entry is made in
``docs/src/modules_schema_configs.py`` for ``Input``.
"""

import logging

import typing as T

# pylint: disable=no-name-in-module
from pydantic import BaseModel, HttpUrl
# pylint: enable=no-name-in-module
import requests

from mitto.script.job import schema


logger = logging.getLogger(__name__)


class Input(BaseModel):
    """Get data from the reqres API"""

    endpoint: str = schema(
        ...,
        """TODO: add docstring here""",
    )

    base_url: HttpUrl = schema(
        "https://reqres.in/api/",
        """TODO: add docstring here""",
    )

    headers: T.Dict = schema(
        {"Content-Type": "application/json"},
        """TODO: The default is a dict, but name is plural.
           can it be a list of dicts?""",
    )

    class Config:
        """ Pydantic Config """

        extras = "forbid"

    def get_items(self, page):
        """get items from reqres api"""
        url = self.base_url + self.endpoint
        response = requests.get(
            url,
            headers=self.headers,
            params={"page": page}
        )
        response.raise_for_status()
        return response.json()["data"]

    def __iter__(self):
        page = 1
        items = self.get_items(page=page)
        while items:
            for item in items:
                yield item
            page += 1
            items = self.get_items(page=page)
