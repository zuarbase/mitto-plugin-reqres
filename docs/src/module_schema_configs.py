"""
JSON Schema documents are created for each of these classes.

The ``docs/src/schemas/index.md`` file and all schema files it references, which
are located in ``docs/src/schemas/`` are created via the contents of
``MODULE_CONFIGS``.
"""

MODULE_CONFIGS = [
    {
        "module": "reqres.types",
        "classes": ["Credentials"],
    },
    {
        "module": "reqres.io.input",
        "classes": ["Input"],
    },
]
