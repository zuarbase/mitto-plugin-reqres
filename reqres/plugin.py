""" Playbook """

import logging
import pathlib

from webapp.plugins import Plugin

from . import forms, settings

logger = logging.getLogger(__name__)

PLUGIN = Plugin(
    name=settings.PLUGIN_NAME,
    title=settings.PLUGIN_TITLE,
    icon_path=(pathlib.Path(__file__).resolve().parent.parent
               / "asset" / "icon.svg"),
)

# pylint: disable=no-member
PLUGIN.playbook.add_screen(form_cls=forms.CredentialsForm)
PLUGIN.playbook.add_screen(form_factory=forms.create_jobs_form)
PLUGIN.playbook.add_screen(form_cls=forms.OutputForm)
