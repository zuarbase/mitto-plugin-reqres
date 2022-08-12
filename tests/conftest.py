import pytest

from starlette.testclient import TestClient

# pylint: disable=unused-import
from mitto.conftest import (  # noqa
    files_fixture
)

import webapp.main


# pylint: disable=redefined-outer-name,unused-argument
@pytest.fixture(scope="function", name="client")
def client_fixture(mocker):
    """
    Because of the way that pytest imports files, it is almost a certainty that
    webapp will be loaded and that init_plugins() will be called before
    plugins_() has executed.  This causes some or all of the V2 plugins to be
    uninitialized.  The following call to init_plugins() ensures that all V2
    plugins get initialized.
    """
    webapp.main.init_plugins(app=webapp.main.app, wsgi_app=mocker.Mock())
    return TestClient(webapp.main.app)
