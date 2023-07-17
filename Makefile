SHELL := /bin/bash
VENV_NAME ?= .venv
PYTHON := $(VENV_NAME)/bin/python3
PIP := $(VENV_NAME)/bin/pip3

.PHONY: all
all: venv dev_install lint

.PHONY: venv
venv: $(VENV_NAME)/bin/activate

$(VENV_NAME)/bin/activate: requirements-dev.txt
	test -d $(VENV_NAME) || virtualenv -p python3 $(VENV_NAME)
	$(PIP) install --upgrade pip
	$(PIP) install -Ur requirements-dev.txt
	touch $(VENV_NAME)/bin/activate
	$(PYTHON) setup.py develop

.PHONY: dev_install
dev_install:
	$(PYTHON) setup.py develop

.PHONY: build
build: venv
	$(PIP) install pyinstaller
	$(VENV_NAME)/bin/pyinstaller --onefile hollywood_agent.py

.PHONY: lint
lint:
	$(PIP) install pylint
	$(VENV_NAME)/bin/pylint --disable=R,C hollywood_agent.py

.PHONY: clean
clean:
	rm -rf $(VENV_NAME)
	rm -rf dist/
	rm -rf build/
