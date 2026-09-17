VENV_NAME = .venv
PYTHON    = $(VENV_NAME)/bin/python
PIP       = $(VENV_NAME)/bin/pip

.PHONY: help venv install linters tests build

help:
	@echo "Makefile commands:"
	@echo "  make venv     - Create virtual environment"
	@echo "  make install  - Install dependencies into venv"
	@echo "  make linters  - Run ruff formatter and linter"
	@echo "  make tests    - Run test suite"
	@echo "  make build    - Build sdist/wheel into dist/"

venv:
	@test -d $(VENV_NAME) || python3 -m venv $(VENV_NAME)
	@echo "Run: source $(VENV_NAME)/bin/activate"

install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt -r requirements-dev.txt

linters:
	$(PYTHON) -m ruff format .
	$(PYTHON) -m ruff check --fix .

tests:
	$(PYTHON) -m pytest

build:
	rm -rf dist
	$(PIP) install --upgrade build
	$(PYTHON) -m build
