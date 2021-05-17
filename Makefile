PROJECT := jsoncomparison
VERSION := $(shell git describe --tags `git rev-list --tags --max-count=1`)

VENV := .venv
REPORTS := .reports

TESTS := tests

clean:
	@rm -rf .mypy_cache
	@rm -rf .pytest_cache
	@rm -rf .coverage
	@rm -rf $(REPORTS)
	@rm -rf $(VENV)

$(VENV):
	poetry install --no-root

$(REPORTS):
	mkdir $(REPORTS)

setup: $(VENV) $(REPORTS)

flake: setup
	poetry run flake8 --max-complexity=10 $(PROJECT) $(TESTS)

mypy: setup
	poetry run mypy $(PROJECT) $(TESTS)

isort: setup
	poetry run isort $(PROJECT) $(TESTS)

isort-lint: setup
	poetry run isort -c $(PROJECT) $(TESTS)

test: setup
	poetry run pytest --cov=$(PROJECT)

format: isort

lint: flake mypy isort-lint

all: format lint test

.DEFAULT_GOAL := all