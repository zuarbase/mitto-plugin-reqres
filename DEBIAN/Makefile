DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
MITTO_HOME ?= $(shell cd $(DIR)/../../mitto && pwd)
include $(MITTO_HOME)/Makefile.include
PYTHONPATH := $(PYTHONPATH):$(shell cd .. && pwd)

NAME := reqres
PACKAGE := mitto-plugin-reqres

VERSION := $(shell PYTHONPATH=$(PYTHONPATH) $(PYTHON3) -c 'import $(NAME); print($(NAME).__VERSION__)')
DIRNAME := $(PACKAGE)-$(VERSION)
INSTALL := $(DIRNAME)/debian/$(PACKAGE).install

all: clean debian/changelog
	mkdir -p $(DIRNAME) opt/$(PACKAGE) opt/mitto
	cp -a ../$(NAME) opt/$(PACKAGE)/
	echo "__VERSION__ = \"$(VERSION)\"" > opt/$(PACKAGE)/$(NAME)/__version__.py
	-find opt/$(PACKAGE) -name __pycache__ \
		-exec rm -rf '{}' ';' >/dev/null 2>&1
	cp -a debian $(DIRNAME)/
	for x in `find opt -type f`; do echo ../$$x /`dirname $$x` >> $(INSTALL); done
	cd $(DIRNAME) && dpkg-buildpackage -i -I -rfakeroot -uc -us
.PHONY: all

debian/changelog:
	$(PYTHON3) $(CHANGELOG_PY) $(NAME) --package=$(PACKAGE)> debian/changelog
.PHONY: debian/changelog

version:
	@echo $(VERSION)
.PHONY: version

clean:
	rm -rf $(PACKAGE)-* opt
	rm -f *.deb *.changes *.dsc *.tar.gz debian/changelog debian/*.install
.PHONY: clean
