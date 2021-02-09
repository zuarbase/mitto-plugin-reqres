import addict

from reqres import ReqResInput

TEST_RESPONSE = {
    "page": 1,
    "per_page": 6,
    "total": 12,
    "total_pages": 2,
    "data": [
        {
            "id": 1,
            "email": "george.bluth@reqres.in",
            "first_name": "fake",
            "last_name": "test",
            "avatar": "https://reqres.in/img/faces/1-image.jpg"
        },
        {
            "id": 2,
            "email": "janet.weaver@reqres.in",
            "first_name": "not",
            "last_name": "real",
            "avatar": "https://reqres.in/img/faces/2-image.jpg"
        },
        {
            "id": 3,
            "email": "emma.wong@reqres.in",
            "first_name": "Emma",
            "last_name": "Wong",
            "avatar": "https://reqres.in/img/faces/3-image.jpg"
        },
    ]
}


def test_reqres_base_url():
    reqres = ReqResInput("users")
    assert reqres.base_url == "https://reqres.in/api/"


def test_get_items(requests_mock):
    reqres = ReqResInput("users")
    url = reqres.base_url + reqres.endpoint
    requests_mock.get(url, json=TEST_RESPONSE)
    assert reqres.get_items(page=1) == TEST_RESPONSE["data"]


def test_iter(mocker):
    # Here's an example of a test that doesn't use requests_mock
    reqres = ReqResInput("users")

    def _request_get(*args, params=None, **kwargs):
        if params["page"] == 1:
            return addict.Dict({
                "status_code": 200,
                "json": lambda: TEST_RESPONSE,
                "raise_for_status": lambda: None
                })
        return addict.Dict({
                "json": lambda: {
                    "data": []
                },
                "raise_for_status": lambda: None
            })
    mocker.patch("requests.get", new=_request_get)
    assert next(iter(reqres)) == TEST_RESPONSE["data"][0]
    assert list(reqres) == TEST_RESPONSE["data"]
