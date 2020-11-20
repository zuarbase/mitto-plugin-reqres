DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
MITTO_HOME ?= $(shell cd $(DIR)/../mitto && pwd)
include $(MITTO_HOME)/Makefile.include

NAME := reqres

all: flake8 pylint coverage DEBIAN

flake8_pkg:
	$(FLAKE8) $(NAME)
.PHONY: flake_pkg

flake8_tests:
	$(FLAKE8) tests/*
.PHONY: flake_tests

flake8: flake8_pkg flake8_tests

pylint_pkg:
	$(PYLINT) $(NAME)
.PHONY: pylint_pkg

pylint_tests:
	$(PYLINT) tests/* --disable=missing-docstring,unused-argument
.PHONY: pylint_tests

pylint: pylint_pkg pylint_tests
.PHONY: pylint

test:
	$(PYTEST) -xv tests
.PHONY: test

coverage:
	$(PYTEST) --cov=reqres --cov-report=term-missing --cov-fail-under=100 tests/
.PHONY: coverage

DEBIAN:
	make -C DEBIAN MITTO_HOME=$(MITTO_HOME)
.PHONY: DEBIAN

publish:
	bash -c 'FILE=`ls ./DEBIAN/mitto*_all.deb` && curl -n -F "file=@$$FILE" $(PUBLISH_TARGET)'
.PHONY: publish

develop:
	ln -snf $(DIR)/$(NAME) $(MITTO_HOME)/plugin/$(NAME)
	ln -snf $(DIR)/static $(MITTO_HOME)/static/plugin/$(NAME)
.PHONY: develop

undevelop:
	rm -f $(MITTO_HOME)/plugin/$(NAME) $(MITTO_HOME)/static/plugin/$(NAME)
.PHONY: undevelop

clean:
	make -C DEBIAN clean
	rm -rf static
	find $(NAME) -name __pycache__ -prune -exec rm -rf '{}' ';'
.PHONY: clean

realclean: clean
	git clean -f -d -X
.PHONY: realclean
