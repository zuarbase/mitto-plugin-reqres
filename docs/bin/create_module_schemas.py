#!/usr/bin/env python3
"""
Creates documentation files for all Pydantic classes specified in
`docs/{src,srcp}/module_schema_configs.py`

This creates Markdown files that contain reST directives.  For this to
work, sphinx must be configured to use process Markdown with the `m2r`
processor.  The default recommonmark processor will not work.
"""

import importlib
import json
import os
import pathlib
import pprint
import re
import sys
import textwrap

import addict


SCHEMAS_DIR = "schemas"


def ensure_python_path():

    docs_bin_dir = pathlib.Path(__file__).resolve()
    mitto_dir = docs_bin_dir.parent.parent
    
    if str(mitto_dir) not in sys.path:
        sys.path.insert(0, str(mitto_dir))
        sys.path.insert(0, ".")
    

def get_src_dir() -> pathlib.Path:
    """
    Return the directory contains source documentation.
    """

    cwd = pathlib.Path().resolve()
    if list(cwd.parts)[-1] not in ["src", "srcp"]:
        print("Must be run from either 'docs/src' or 'docs/srcp'")
        sys.exit(1)

    return cwd
    

def get_src_schemas_dir() -> pathlib.Path:
    """
    Return the directory that will contain the schemas that are to be created.
    """

    return get_src_dir() / SCHEMAS_DIR


class ModuleDocumentation:
    """
    Creates JSON schema files and related documentation files.
    """

    # This is kludgy...  `module_index_paths` accumulates all list of all
    # tuples generated by class instances.
    # A list of tuples of the form `(module, path)`, where `module` is the name
    # of a Python module and `path` is a relative path to the index.md file
    # containing JSON schema documentation for the module.
    module_index_paths = list()

    def __init__(self, module_config):

        self.module = module_config["module"]
        self.classes = module_config["classes"]
        self.src_schemas_dir = get_src_schemas_dir()
        self.module_schemas_dir = self.get_module_schemas_dir()

    def get_module_schemas_dir(self):
        """
        Return the directory that will contain JSON schema files for the module,
        creating it if necessary.
        """

        module_schemas_dir = self.src_schemas_dir

        for part in self.module.split("."):
            module_schemas_dir /= part

        module_schemas_dir.mkdir(parents=True, exist_ok=True)
        return module_schemas_dir

    def create_module_index(self, class_schema_paths):
        """
        Creates `docs/schemas/...path.../{module}/index.md` which will contain
        reST directives for each of the module's Pydantic classes specified in
        MODULE_CONFIGS.

        Returns a tuple of the form `(module, path)`, where `path` is a relative
        path to the module's `index.md`.
        """

        preamble = """
           # Module - {module}

           """

        content = textwrap.dedent(preamble.format(module=self.module))

        for klass, path in class_schema_paths:
            content += f".. jsonschema:: {path.name}\n\n" 

        index_file = self.module_schemas_dir / "index.md"
        index_file.write_text(content)

        rel_path = index_file.relative_to(self.src_schemas_dir)
        info = (self.module, rel_path)
        return info

    def create_class_schemas(self):
        """
        Creates a `{class}.json` file for each class.
        Returns a list of tuples.
        """

        class_schema_paths = list()
        for klass in self.classes:
            path = self.create_class_schema(klass)
            info = (klass, path)
            class_schema_paths.append(info)

        return class_schema_paths

    def create_class_index(self, klass, targets):

        class_schema = f"{klass}.json"

        index_file_name = f"index_{klass}.md"
        index_file = open(self.get_module_schemas_dir() / index_file_name, "w")

        index_file.write(f"# Class Index: {self.module}.{klass}\n\n")

        for target in targets:
            index_file.write(f".. jsonschema:: {class_schema}{target}\n\n\n")

        index_file.close()


    def create_class_schema(self, klass):
        """
        Creates a `{klass}.json` file containing the JSON Schema for `klass`.
        Returns a relative path to the created file.
        """

        try:
            module = importlib.import_module(self.module)
        except ImportError:
            raise ImportError(f"Error: Unable to import {self.module}")

        klass_ = getattr(module, klass)
        schema, targets = self.add_targets_to_schema(klass_.schema())

        module_schemas_dir = self.get_module_schemas_dir()
        schema_file = module_schemas_dir / f"{klass}.json"
        schema_file.write_text(json.dumps(schema, indent=4))

        self.create_class_index(klass, targets)

        rel_path = schema_file.relative_to(self.src_schemas_dir)

        return rel_path


    @classmethod
    def create_schemas_index(cls):
        """
        Creates a top-level index with links to each module's JSON schema
        documentation: `docs/{src,srcp}/schemas/index.md`

        Called only after all module/class documentation has been created by
        `create()`.
        """

        preamble = """
           # JSON Schemas by Module

           """

        content = textwrap.dedent(preamble)
        for module, path in ModuleDocumentation.module_index_paths:
            content += f"* [{module}]({path})\n\n"

        index_file = get_src_schemas_dir() / "index.md"
        index_file.write_text(content)

    def create(self):
        """
        Creates module-level documentation for the specified module and classes.
        """
        class_schema_paths = self.create_class_schemas()
        info = self.create_module_index(class_schema_paths)
        ModuleDocumentation.module_index_paths.append(info)

    def add_targets_to_schema(self, schema):
        """
        For references in JSON schema documents to work properly, each member of
        `"definitions"` must have a `$$target` added.

        Returns a tuple of the form `(schema, targets)`, where `schema` is the
        modified schema and `targets` is a list of the targets that were added.
        """

        targets = list()

        try:
            for key, value in schema["definitions"].items():
                target = f"#/definitions/{key}"
                value["$$target"] = target
                targets.append(target)
        except KeyError:
            # "definitions" is not present in schema
            pass

        return schema, targets



if __name__ == '__main__':

    """
    Creates all json_schema documentation files specified in json_schemas.
    Must be run from within docs/src or docs/srcp.
    """

    cwd = pathlib.Path().resolve()
    mitto_dir = cwd.parent.parent
    sys.path.insert(0, str(mitto_dir))
    sys.path.insert(0, ".")

    try:
        from module_schema_configs import MODULE_CONFIGS
    except ModuleNotFoundError:
        print(f"no MODULE_CONFIGS, skipping schema creation.")
        sys.exit(0)

    for module_config in MODULE_CONFIGS:
        md = ModuleDocumentation(module_config)
        md.create()

    ModuleDocumentation.create_schemas_index()
    sys.exit(0)
