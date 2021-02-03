import pytest
import requests

from reqres import ReqResInput

TEST_RESPONSE = {
    "page": 1,
    "per_page": 6,
    "total": 12,
    "total_pages": 2,
    "data": [
        {"id": 1, "email": "george.bluth@reqres.in", "first_name": "George", "last_name": "Bluth", "avatar": "https://reqres.in/img/faces/1-image.jpg"},
        {"id": 2, "email": "janet.weaver@reqres.in", "first_name": "Janet", "last_name": "Weaver", "avatar": "https://reqres.in/img/faces/2-image.jpg"},
        {"id": 3, "email": "emma.wong@reqres.in", "first_name": "Emma", "last_name": "Wong", "avatar": "https://reqres.in/img/faces/3-image.jpg"},
        {"id": 4, "email": "eve.holt@reqres.in", "first_name": "Eve", "last_name": "Holt", "avatar": "https://reqres.in/img/faces/4-image.jpg"},
        {"id": 5, "email": "charles.morris@reqres.in", "first_name": "Charles", "last_name": "Morris", "avatar": "https://reqres.in/img/faces/5-image.jpg"},
        {"id": 6, "email": "tracey.ramos@reqres.in", "first_name": "Tracey", "last_name": "Ramos", "avatar": "https://reqres.in/img/faces/6-image.jpg"}
    ],
    "support": {"url": "https://reqres.in/#support-heading", "text": "To keep ReqRes free, contributions towards server costs are appreciated!"}
}

def test_reqres_base_url():
    reqres = ReqResInput("users")
    assert reqres.base_url == "https://reqres.in/api/"

def test_get_items(requests_mock):
    reqres = ReqResInput("users")
    url = reqres.base_url + reqres.endpoint
    requests_mock.get(url, json=TEST_RESPONSE)
    assert reqres.get_items() == TEST_RESPONSE

def test_get_items_with_page(requests_mock):
    reqres = ReqResInput("users")
    url = reqres.base_url + reqres.endpoint
    requests_mock.get(url, json=TEST_RESPONSE)
    with_page = reqres.get_items(page=2)
    assert with_page == TEST_RESPONSE
