install:
	uv sync

build:
	uv build

package-install:
	uv tool install dist/*.whl

run:
	uv run page-loader $(ARGS)

lint:
	uv run ruff check page_loader tests

lint-fix:
	uv run ruff check --fix page_loader tests

test:
	uv run pytest

test-coverage:
	uv run pytest --cov=page_loader --cov-report=xml --cov-report=term

check: lint test

.PHONY: install build package-install run lint lint-fix test test-coverage check
