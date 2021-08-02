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


def test_two(xsession, client):
    """
    Test successul creds
    """

    state = provide_creds(client)
    state = choose_config(client, state)
    output(client, state)


def provide_creds(client):
    """
    Provide creds on first page of wizard.
    """

    ##################################################
    # get initial state / Page_0
    this_screen = 0

    resp = client.get(WIZARD_ENDPOINT)
    assert resp.status_code == 200
    state = resp.json()
    assert state["screen_index"] == this_screen

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
    state["screens"][this_screen]["data"] = data

    state["action"] = ActionEnum.next
    resp = client.post(WIZARD_ENDPOINT, json=state)
    assert resp.status_code == 200

    state = resp.json()

    # no errors on current screen
    assert state["screens"][this_screen]["errors"]["detail"] == []
    # screen_index changed to next page
    assert state["screen_index"] == this_screen + 1

    return state


def choose_config(client, state):
    """
    Choose a job config.
    """

    ##################################################
    # Screen 1
    #    - get email/password
    #    - simulate user data entry followed by "Next" click

    this_screen = 1

    # confirm that one of the configs is among choices
    assert "unknown.hjson" in state["screens"][this_screen][
        "schema"]["properties"]["job_choices"]["items"]["enum"]

    # simulate user selecting job choice
    state["screens"][this_screen]["data"]["job_choices"] = [
        "unknown.hjson",
    ]

    # simulate user clicking 'next'
    state["action"] = ActionEnum.next
    resp = client.post(WIZARD_ENDPOINT, json=state)

    state = resp.json()

    assert resp.status_code == 200
    assert state["screens"][this_screen]["errors"]["detail"] == []
    assert state["screen_index"] == this_screen + 1
    return state


def output(client, state):
    """
    Provide db params and create job.
    """

    this_screen = 2

    # simulate user providing db info
    data = {
        "dbo_choice": False,
        "dbo": "postgresql://localhost/analytics-test",
        "schema": "reqres_test",
        "tablename": "reqres_test",
    }
    state["screens"][this_screen]["data"] = data

    # simulate user clicking 'done'
    state["action"] = ActionEnum.done
    resp = client.post(WIZARD_ENDPOINT, json=state)

    state = resp.json()

    assert resp.status_code == 200
    assert state["screen_index"] == this_screen
    assert state["screens"][this_screen]["errors"]["detail"] == []
    assert state["screens"][this_screen]["next"] == "Done"

    # confirm that a job was actually created within mitto
    assert state["job_id"]
