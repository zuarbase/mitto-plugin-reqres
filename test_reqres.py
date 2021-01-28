import pytest

from reqres import ReqResInput

def test_reqres():
    reqres = ReqResInput("users")
    assert reqres.base_url == "https://reqres.in/api/"
