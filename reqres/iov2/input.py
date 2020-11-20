"""Get data from the reqres API"""

import logging
import requests

logger = logging.getLogger(__name__)


class ReqResInput:
    """Get data from the reqres API"""

    def __init__(
            self,
            endpoint):
        # pylint: disable=too-many-locals
        self.endpoint = endpoint
        self.base_url = "https://reqres.in/api/"
        self.headers = {"Content-Type": "application/json"}

    def get_items(self, page=None):
        """get items from reqres api"""
        page_string = ""
        if page is not None:
            page_string = "?page={}".format(page)
        url = self.base_url + self.endpoint + page_string

        try:
            response = requests.get(url, headers=self.headers)
        except requests.exceptions.RequestException:
            print("Requests error")
        json = response.json()
        return json

    def __iter__(self):
        page = 1
        items = self.get_items(page=page)
        while items:
            for item in items["data"]:
                yield item
            page += 1
            items = self.get_items(page=page)
            if not items["data"]:
                items = {}
