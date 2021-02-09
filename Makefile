PACKAGE := reqres
SHELL := /bin/bash

all: flake8 pylint coverage
.PHONY: all

flake8:
	flake8 $(PACKAGE).py test_reqres.py
.PHONY: flake8

pylint: pylint_pkg pylint_tests
.PHONY: pylint

pylint_pkg:
	pylint $(PACKAGE)
.PHONY: pylint_pkg

pylint_tests:
	pylint test_reqres.py --disable=missing-docstring,duplicate-code,unused-argument
.PHONY: pylint_test

test:
	pytest -xv tests
.PHONY: test

coverage:
	pytest --cov=$(PACKAGE) --cov-report=term-missing --cov-fail-under=100 test_reqres.py
.PHONY: coverage

freeze:
	pyenv/bin/pip freeze | egrep -v "$(PACKAGE)|flake8|pylint|pytest|pkg-resources" > requirements.txt
.PHONY: freeze

pyenv:
	virtualenv -p python3 pyenv
	pyenv/bin/pip install -e .[dev,prod]
	pyenv/bin/pip install -r requirements.txt
.PHONY: pyenv
