# pylint: disable=unused-argument,unused-import
import tempfile

import hjson

import pytest

from mitto.conftest import engine_fixture, xsession_fixture  # noqa: F401
from mitto.playbook import ActionEnum
from webapp.plugins import V2_PLUGINS_PREFIX
from reqres import PLUGIN_NAME
from reqres.types import Credentials

WIZARD_ENDPOINT = f"{V2_PLUGINS_PREFIX}/{PLUGIN_NAME}"


def test_one(client):
    """
    Confirm plugin is installed
    """

    plugin_name = PLUGIN_NAME.replace("/", "")

    resp = client.get(V2_PLUGINS_PREFIX)
    assert resp.status_code == 200

    assert plugin_name in resp.json()["plugins"]


def show(state):
    import copy
    nstate = copy.deepcopy(state)
    nstate["icon"] = "<svg-icon>"
    return nstate


def provide_creds(client, status_code=200):
    """
    Provide creds on first page of wizard.
    """

    ##################################################
    # get initial state / Page_0

    resp = client.get(WIZARD_ENDPOINT)
    assert resp.status_code == 200
    state = resp.json()
    assert state["screen_index"] == 0

    ##################################################
    # Screen 0
    #    - get email/password
    #    - simulate user data entry followed by "Next" click

    data = {
        "credentials": {
            "email": "michael.lawson@reqres.in",
            "password": "PassworD",
        },
    }

    state["screens"][0]["data"] = data
    state["action"] = ActionEnum.next
    resp = client.post(WIZARD_ENDPOINT, json=state)
    assert resp.status_code == status_code

    state = resp.json()

    if status_code == 200:
        # no errors on current screen
        assert state["screens"][0]["errors"]["detail"] == []
        # screen_index changed to next page
        assert state["screen_index"] == 1

    return state


def test_two(xsession, client):
    """
    Test successul creds
    """

    state = provide_creds(client)
    state = choose_config(client, state)
    db_done(client, state)

def choose_config(client, state):
    """
    Choose a job config.
    """

    # confirm that one of the configs is among choices
    assert "unknown.hjson" in state["screens"][1]["schema"][
        "properties"]["job_choices"]["items"]["enum"]

    # simulate user selecting job choice
    state["screens"][1]["data"]["job_choices"] = ["unknown.json"]

    # simulate user clicking 'next'
    state["action"] = ActionEnum.next
    resp = client.post(WIZARD_ENDPOINT, json=state)

    state = resp.json()

    assert resp.status_code == 200
    assert state["screens"][1]["errors"]["detail"] == []
    assert state["screen_index"] == 2

    return state


def db_done(client, state):
    """
    Choose a job config.
    """

    # confirm that one of the configs is among choices
    assert "unknown.hjson" in state["screens"][1]["schema"][
        "properties"]["job_choices"]["items"]["enum"]

    # simulate user selecting job choice
    state["screens"][1]["data"]["job_choices"] = ["unknown.json"]

    # simulate user clicking 'next'
    state["action"] = ActionEnum.next
    resp = client.post(WIZARD_ENDPOINT, json=state)

    state = resp.json()

    assert resp.status_code == 200
    assert state["screens"][1]["errors"]["detail"] == []
    assert state["screen_index"] == 2

    return state


def test_three(xsession, client):
    """
    Test attempt to create duplicate job name
    """

    title = "Job Title"

    # first attempt succeeds
    create_job(client, title=title)

    with pytest.raises(AssertionError):
        # duplicate job name failure
        create_job(client, title=title)


def test_four(xsession, client):
    """
    Create job with invalid config.
    """

    # test invalid HJSON
    invalid_json = "{"
    create_job(client, config=invalid_json, status_code=422)

    # test valid HJSON but invalid job config (i.e. dict)
    invalid_config = "1"
    create_job(client, config=invalid_config, status_code=422)

    # a file that does not exist
    temp_file = tempfile.NamedTemporaryFile()
    missing_config_file_name = temp_file.name
    temp_file.close()

    create_job(client, config=missing_config_file_name, status_code=422)
