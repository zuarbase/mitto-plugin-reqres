"""
ReqRes Inputter

By convention, a plugin's inputter is located in
`<plugin-name>/<plugin-name>/iov2/input.py`; it is typically named `Input`.
Some plugins have more than one iputters, depending upon their needs.
"""

import logging
import requests

import typing as T

import pydantic

from mitto.script.job import schema


logger = logging.getLogger(__name__)


class Input(pydantic.BaseModel):
    """Get data from the reqres API"""

    endpoint: str = schema(
        ...,
        """TODO: add docstring here""",
    )

    base_url: pydantic.HttpUrl = schema(
        "https://reqres.in/api/",
        """TODO: add docstring here""",
    )

    headers: T.Dict = schema(
        {"Content-Type": "application/json"},
        """TODO: The default is a dict, but name is plural.  can it be a list of dicts?""",
    )

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
