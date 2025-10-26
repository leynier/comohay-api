HOST = localhost
PORT = 8000

install:
	uv sync

tests: install
	uv run flake8 . --count --show-source --statistics --max-line-length=88 --extend-ignore=E203 --exclude=.venv
	uv run black . --check --exclude=.venv
	uv run isort . --profile=black --skip=.venv
	uv run pytest

run: install
	uv run uvicorn api.main:app --reload --host ${HOST} --port ${PORT}
