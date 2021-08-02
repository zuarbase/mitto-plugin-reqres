"""
Wizard forms for ReqRes plugin
"""

import hjson
import logging
import pathlib
import pprint

import typing as T

import pydantic

from mitto.exc import PluginError
from mitto.job import install
from mitto.jsoneditor import PrivateBaseModel
from mitto.model import bind
from mitto.playbook import Screen
from mitto.script.job import schema
from mitto.settings import ANALYTICS_DATABASE_URL

from reqres.client import get_token
from reqres.types import Credentials
from reqres.utils import get_conf_templates, render_template


logger = logging.getLogger(__name__)


EXAMPLE_URI = ("e.g.: postgresql://[user[:password]@][netloc][:port]"
               "[/dbname][?param1=value1&...]")


class CredentialsForm(PrivateBaseModel):
    """ ReqRes user credentials """

    credentials: Credentials = schema(
        ...,
        ""
    )



class XCredentialsForm(PrivateBaseModel):
    """ ReqRes user credentials """

    credentials: Credentials = schema(
        ...,
        ""
    )

    class Config(PrivateBaseModel.Config):
        """
        Config.title is displayed as the Wizard title.
        """

        title = "Specify the ReqRes account and password"

    def post_validate(self, screens: T.List[Screen]):
        """Final email/password validation.

        In general, when the user clicks "Done", Pydantic validates the form
        according to the form's definition.  If the Pydantic validation is
        successful, post_validate() is called, if it exists.

        In this instance, when the user clicks "Done", Pydantic validates the
        email/password according to the Credentials implementation.  If the
        Pydantic validation is successful, this function is called.

        Here, the credentials are passed to the API to obtain an auth token.
        If the credentials are invalid (e.g, the account has been disabled),
        the PluginError exception displays a message to the user; they
        are not allowed to progress to the next screen of the wizard.
        """

        self.credentials.token = get_token(screens[0].form_inst.credentials)
        if self.credentials.token is None:
            raise PluginError("invalid email or password")


def create_jobs_form(screens: T.List[Screen]):
    """Creates a JobsForm class dynamically.

    This form can only be created at runtime because it presents the
    job templates present in the `conf` subdirectory.  If a user-writeable
    directory were used instead of `reqres/conf`, this implementation would
    allow users to add config files as needed and have them reflected
    automatically in the wizard.
    """

    _ = screens

    templates_ = get_conf_templates()

    class JobsForm(PrivateBaseModel):
        """ Select one or more jobs to create """

        job_choices: T.List[str] = schema(
            ...,
            """
            Select one or more jobs to create.
            """,
            title="Available jobs",
            format="select",
            items={"type": "string"},
            uniqueItems=True,
        )

        @pydantic.validator("job_choices", allow_reuse=True)
        def job_choices_validator(
                # pylint: disable=no-self-argument
                cls, val
        ):
            """ Pydantic validator """

            if len(val) == 0:
                raise ValueError("at least one job must be selected")
            return val

        class Config(PrivateBaseModel.Config):
            """
            Config.title is displayed as the Wizard title.
            """

            title = "Choose jobs "

        @classmethod
        def schema(cls, by_alias: bool = True):
            """ Override schema to allow dynamic items """
            schema_dict = super().schema(by_alias)
            schema_dict["properties"]["job_choices"]["items"].update(
                enum=list(templates_.keys())
            )
            return schema_dict

        @property
        def templates(self):
            """ Return available templates """
            return templates_

    return JobsForm


class OutputForm(PrivateBaseModel):
    """"""  # pylint: disable=empty-docstring

    title_prefix: str = schema(
        "ReqRes",
        """
        Prefix for job titles
        """,
    )

    dbo_choice: bool = schema(
        True,
        """
        """,
        title="Use default database URI",
        type="boolean",
        format="checkbox",
    )

    dbo: str = schema(
        ANALYTICS_DATABASE_URL,
        "",
        min_length=1,
        title="Custom database URI",
        options={
            "inputAttributes": {
                "placeholder": EXAMPLE_URI,
            },
            "dependencies": {
                "dbo_choice": False,
            },
        },
    )

    schema_: str = schema(
        ...,
        "",
        alias="schema",
        min_length=1,
    )

    tablename: str = schema(
        ...,
        "",
        min_length=1,
    )

    class Config(PrivateBaseModel.Config):
        """
        Config.title is displayed as the Wizard title.
        """

        title = "Select oputput"

    def install_job(self, job_config: T.Dict, just_log=True):
        """ Register the job with Mitto """

        # pylint: disable=cyclic-import,import-outside-toplevel
        from reqres.plugin import PLUGIN
        # pylint: enable=cyclic-import,import-outside-toplevel
        job_config["name"] = PLUGIN.job_name(job_config["title"])

        if just_log:
            logger.info(pprint.pprint(job_config, indent=4))
            return

        bind()

        try:
            result = install(job_config)

        # pylint: disable=broad-except
        except Exception as exc:
            raise PluginError(exc)

        logger.info("created job: %s", result)

        # Put id of the successfully created job into the playbook which will
        # be sent to the frontend so that it can redirect to the job's
        # detail page
        # pylint: disable=no-member
        PLUGIN.set_job_id(result["id"])

    def post_validate(self, screens: T.List[Screen]):
        """ Create the job(s) """

        jobs_form = screens[1].form_inst
        output_form = screens[2].form_inst
        job_choices = jobs_form.job_choices

        for job_choice in job_choices:

            title = (output_form.title_prefix + " "
                     if output_form.title_prefix else "")
            title += pathlib.Path(job_choice).stem

            params = {
                "title": title,
                "dbo": output_form.dbo,
                "schema": output_form.schema_,
                "tablename": output_form.tablename,
            }

            job_config_template = jobs_form.templates[job_choice]
            job_config = hjson.loads(
                render_template(job_config_template, params)
            )
            self.install_job(job_config, just_log=False)
