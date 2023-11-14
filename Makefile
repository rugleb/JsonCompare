PROJECT := jsoncomparison

VENV := .venv
REPORTS := .reports

TESTS := tests
PY_FILES := $(shell find $(PROJECT) $(TESTS) -name "*.py")

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

bandit: setup
	poetry run bandit -rq $(PROJECT) $(TESTS)

isort: setup
	poetry run isort $(PROJECT) $(TESTS)

isort-lint: setup
	poetry run isort -c $(PROJECT) $(TESTS)

trailing: setup
	@poetry run add-trailing-comma $(PY_FILES) --exit-zero-even-if-changed

trailing-lint: setup
	@poetry run add-trailing-comma $(PY_FILES)

test: setup
	poetry run pytest --cov=$(PROJECT)

format: isort trailing

lint: flake mypy bandit isort-lint trailing-lint

all: format lint test

.DEFAULT_GOAL := all
