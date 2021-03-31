################################################################################
# Public documentation is published to www.zuar.com using 'rsync'.
# Private documentation is published to secure S3 bucket using 'rclone'.
#
# SETUP
#
# Public
#    1. ssh credentials for www.zuar.com must be present in ~/.ssh and
#       ~/.ssh/config must be properly setup for rsync to work.
#
# Private
#    1. AWS credentials must be setup in ~/.aws/credentials.
#       They should look something like this:
#           aws_access_key_id = AIAKJNMIB77ACMSYSEWA 
#	    aws_secret_access_key = jP1Qp4lcddBFxlvEdOjK0Jx1YrCAj8TmAW3kDi3o
#           region = us-east-1
#    2. rlcone must be setup for S3.  ~/.config/rclone/rclong.conf should look
#       something like this:
#	   [s3private]
#	   type = s3
#	   provider = AWS
#	   env_auth = true
#	   acl = private
#
################################################################################


# Usage:
#
# To be run from developer machine.
#
# 	Setup:
#		'cd docs'
#       	'make pyenv'
#
#	Public Documentation:
#		'make clean'
#		'make all'
#	        'make publish'
#
#	Private Documentation:
#	        'make PVT=y clean'
#	        'make PVT=y all'
#       	'make PVT=y publish'
#
#	To view html locally:
#		'make serve', or
#		'make PVT=y serve'
#

PROJ = reqres

VIRTUAL_ENV ?= $(MITTO_HOME)/pyenv
PYENV := $(VIRTUAL_ENV)
PIP := $(PYENV)/bin/pip3

SPHINXOPTS    = -n -j auto -E
SPHINXBUILD   = sphinx-build

# Defines upload destination on AWS S3
AWS_PROFILE = zuar
S3_BUCKET_PUB  = s3public:zuar.com
S3_BUCKET_PVT  = s3private:zuar-private-docs

ifdef PVT
# Publish to private S3 bucket
SOURCEDIR        = srcp
BUILDDIR         = buildp
# note absence of trailing slash
HTMLDIR          = $(BUILDDIR)/html
PUBLISH_TARGET   = $(S3_BUCKET_PVT)/docsp/$(PROJ)
PUBLISH_CMD      = rclone sync
ROOT_URL         = 
else
# Publish to www.zuar.com
SOURCEDIR        = src
BUILDDIR         = build
# note added trailing slash for rsync
HTMLDIR          = $(BUILDDIR)/html/
PUBLISH_TARGET   = www.zuar.com:static/w3/api/mitto/plugin/$(PROJ)
PUBLISH_CMD      = rsync -arv --delete
ROOT_URL         = https://www.zuar.com/api/mitto/plugin/$(PROJ)/
endif

SCHEMASDIR = schemas

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
.PHONY: help

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
.PHONY: Makefile

pyenv:
	$(PIP) install -r requirements.txt
.PHONY: pyenv

all: schemas html sitemap
.PHONY: all

# For local viewing of created documents
serve:
	cd $(HTMLDIR); python3 -m http.server 8000
.PHONY: serve

publish:
	$(PUBLISH_CMD) $(HTMLDIR) $(PUBLISH_TARGET)
.PHONY: publish

clean:
	@$(SPHINXBUILD) -M clean "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	@-find $(SOURCEDIR)/$(SCHEMASDIR)/* -type f -and -not -name \@Readme.md -delete
	@-find $(SOURCEDIR)/$(SCHEMASDIR)/* -type d -delete
	@rm -rf $(SOURCEDIR)/__pycache__
	@rm -rf $(BUILDDIR)
.PHONY: clean

schemas:
	cd $(SOURCEDIR); ../bin/create_module_schemas.py
.PHONY: schemas

sitemap:
ifdef ROOT_URL
	bin/sitemap.py $(ROOT_URL) $(HTMLDIR) _sources _static templates > "$(HTMLDIR)sitemap.xml"
endif
.PHONY: sitemap

print-%:
	@echo '$*=$($*)'
	@echo '  origin = $(origin $*)'
	@echo '  flavor = $(flavor $*)'
	@echo '   value = $(value  $*)'
