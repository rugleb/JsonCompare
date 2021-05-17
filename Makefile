PROJECT := jsoncomparison
VERSION := $(shell git describe --tags `git rev-list --tags --max-count=1`)

VENV := .venv
REPORTS := .reports

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

test: setup
	poetry run pytest --cov=$(PROJECT)

all: test

.DEFAULT_GOAL := all
