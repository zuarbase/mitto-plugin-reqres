## ReqRes Wizard

We'll create an example wizard that does the following:

1. Prompts the user for their credentials
2. Ensures the credentials are valid by obtaining an access token.
3. Lists available job configurations and allows the user to choose
   one or more.
4. Allows the user to specify database output parameters.
5. For each chosen job configuration
   1. Creates a Mitto job configuration by performing template
      substitution on the specified template with the input
      parameters.
   2. Installs the job in Mitto so that it can be run later.	

More complex wizards could:
- present the user with a list of existing named credentials to choose from
- allow saving new named credentials
- inspect error responses from the API for additional, more specific, error
  and display that to the user.

### Background

Mitto wizards are specified primarily through the creation of Pydantic
classes.  Usually one or more classes per screen of the wizard.  The
classes provide the following:
* Wizard, screen, and field titles
* Validation of input fields using Python type hints
* Validation of input fields using Python validators that can execute
  arbitrary Python code (e.g., perform API calls to validate
  credentials, etc.)
* Automatic generation of documentation
* Automatic generation of the wizard's user interface.  This is done
  by generating JSON Schema from the Pydantic classes which is then
  displayed to the user via JSON Editor.

The following resources will be helpful in writing wizards:

* **Python type hints**
  * https://docs.python.org/3/library/typing.html
  * https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html
* **Pydantic**
  * https://pydantic-docs.helpmanual.io/
* **JSON Schema**
  * https://json-schema.org/
* **JSON Editor**
  * https://github.com/json-editor/json-editor
  * https://pmk65.github.io/jedemov2/dist/demo.html

### Implementation

At a high level, the following must be added to the initial `reqres`
job:

* Creation of two job configuration templates in `reqres/conf`.
* Implementation of a `ReqRes` client in `reqres.py` which validates
  credentials.  Long-term, the inputter should be modified to use this
  client, if this example is to model typical Mitto plugins.
* Definition of the screens used by the wizard to collect data from
  the user. There is a 1:1 correspondence between forms and wizard
  screens.  This is in `reqres/forms.py`.
* Because it is used in more than just forms, a `Credentials` class
  for `reqres` credentials is defined in `reqres/types.py`.
  `Credentials` are used by forms as well as `ReqResClient`.
* `reqres/icon.svg` is the SVG icon displayed by Mitto for this
  wizard.
* Finally, `reqres/__init__.py`.  This is the means through which
  Mitto loads the plugin into the Mitto execution environment.