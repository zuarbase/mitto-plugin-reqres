"""
ReqRes utils
"""

import pathlib

import typing as T

import jinja2


def get_conf_templates() -> T.Dict[str, str]:
    """ Return dict of config file names and their contents """

    templates = dict()
    conf_dir = pathlib.Path(__file__).parent / "conf"
    for conf_file in conf_dir.glob("*.json"):
        templates[conf_file.name] = conf_file.read_text()

    return templates


def render_template(template_str: str, substitutions: T.Dict[str, str]) -> str:
    """ Perform template substitutions """

    template = jinja2.Template(template_str)
    return template.render(**substitutions)
