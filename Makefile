# Makefile for fabric8-analytics tagger
#
# Author: Fridolin Pokorny <fridolin@redhat.com>

TEMPFILE := $(shell mktemp -u)

.PHONY: install clean uninstall venv check doc docs html api coala pylint pydocstyle pytest

install:
	pip3 install -r requirements.txt
	python3 setup.py install

venv:
	virtualenv -p python3 venv && source venv/bin/activate && pip3 install -r requirements.txt
	@echo "Run 'source venv/bin/activate' to enter virtual environment and 'deactivate' to return from it"

devenv:
	pip3 install -r requirements.txt -r dev_requirements.txt

clean:
	find . -name '*.pyc' -or -name '__pycache__' -print0 | xargs -0 rm -rf
	rm -rf venv venv-coala
	rm -rf dist *.egg-info build

pylint:
	@echo ">>> Running pylint"
	pylint f8a_tagger f8a_tagger_cli.py

coala:
	@# We need to run coala in a virtual env due to dependency issues
	@echo ">>> Preparing virtual environment for coala" &&\
	  [ -d venv-coala ] || virtualenv -p python3 venv-coala &&\
	  . venv-coala/bin/activate && pip3 install coala-bears "setuptools>=17.0" &&\
	  echo ">>> Running coala" &&\
	  venv-coala/bin/python3 venv-coala/bin/coala --non-interactive

pydocstyle:
	@echo ">>> Running pydocstyle"
	pydocstyle f8a_tagger

check: pylint pydocstyle coala

test: check
