"""Get data from the reqres API"""

import logging
import requests

logger = logging.getLogger(__name__)


class ReqResInput:
    """Get data from the reqres API"""

    def __init__(
            self,
            endpoint):
        self.endpoint = endpoint
        self.base_url = "https://reqres.in/api/"
        self.headers = {"Content-Type": "application/json"}

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
