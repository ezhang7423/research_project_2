.ONESHELL:
#* Variables
SHELL := bash
PYTHON := python
PYTHONPATH := `pwd`
UV := uv

#* Installation
.PHONY: install
install:
	! type -P $(UV) &> /dev/null && { echo "Please install uv (https://docs.astral.sh/uv/)"; exit 1; }
	$(UV) python install 3.11
	$(UV) venv -c --python 3.11
	$(UV) sync
	$(UV) run pre-commit install

.PHONY: lock
lock:
	! type -P $(UV) &> /dev/null && { echo "Please install uv (https://docs.astral.sh/uv/)"; exit 1; }
	$(UV) lock
	$(UV) export --format requirements.txt --no-dev --no-hashes --no-emit-project -o requirements.txt

#* Linting
.PHONY: lint
lint: test codestyle mypy


.PHONY: test
test:
	PYTHONPATH=$(PYTHONPATH) $(UV) run pytest -c pyproject.toml tests/

.PHONY: mypy
mypy:
	$(UV) run mypy --config-file pyproject.toml ./

#* Formatters
.PHONY: codestyle
codestyle:
	$(UV) run pyupgrade --exit-zero-even-if-changed --py38-plus **/*.py
	$(UV) run isort --settings-path pyproject.toml ./
	$(UV) run black --config pyproject.toml ./

.PHONY: formatting
formatting: codestyle
