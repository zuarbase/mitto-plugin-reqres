"""
ReqRes client
"""

import json

import typing as T

import requests

from reqres.types import Credentials


def get_token(credentials: Credentials) -> T.Optional[str]:
    """
    Login and get an access token.  Returns None
    if credentials are invalid.
    """

    client = ReqResClient(credentials)
    return client.login()


def get_colors(credentials: Credentials):
    """
    Returns a list of color names.
    """

    client = ReqResClient(credentials)
    client.login()
    return sorted(client.get_colors())


class ReqResClient:
    """
    Bare-bones client for fictitious API simulated with ReqRes.
    To keep it simple, many many real-world issues are ignored.
    E.g., efficiency, errors, paging, etc.
    """

    api_base_url = "https://reqres.in/api"

    def __init__(self, credentials: Credentials):
        self.credentials = credentials
        self.headers = dict()

    def login(self) -> T.Optional[str]:
        """
        Login to API, get/save auth token, return it.
        """

        self.credentials.token = None

        url = self.api_base_url + "/login"
        payload = self.credentials.dict()
        resp = requests.post(url, data=payload)
        if resp.status_code == 200:

            try:
                data = resp.json()
                self.credentials.token = data.get("token", None)

                # Example of adding auth headers; ReqRes ignores this
                self.headers = {
                    "email": self.credentials.email,
                    "auth-token": self.credentials.token,
                }

            except json.JSONDecodeError:
                pass

        return self.credentials.token

    def get_colors(self) -> T.List[str]:
        """
        Returns a list of color names.
        """

        url = self.api_base_url + "/colors"
        resp = requests.get(url, headers=self.headers)
        resp.raise_for_status()

        data = resp.json()
        data = data.get("data", list())
        color_list = [item["name"] for item in data]
        return color_list
