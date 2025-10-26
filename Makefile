HOST = localhost
PORT = 8000

install:
	uv sync

tests: install
	uv run ruff check .
	uv run ruff format --check .
	uv run pytest

format: install
	uv run ruff check --fix .
	uv run ruff format .

run: install
	uv run uvicorn api.main:app --reload --host ${HOST} --port ${PORT}
