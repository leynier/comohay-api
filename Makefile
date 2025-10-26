HOST = localhost
PORT = 8000

install:
	uv sync

tests: install
	uv run flake8 . --count --show-source --statistics --max-line-length=88 --extend-ignore=E203 --exclude=.venv
	uv run black . --check --exclude=.venv
	uv run isort . --profile=black --skip=.venv
	uv run pytest --cov=./ --cov-report=xml

export:
	uv export --no-hashes -o requirements.txt

export_and_commit: export
	git config --global user.name 'leynier'
	git config --global user.email 'leynier41@gmail.com'
	git add requirements.txt
	git commit --allow-empty -m "Update requirements.txt"
	git push

update_index:
	cp README.md docs/index.md

update_index_and_commit: update_index
	git config --global user.name 'leynier'
	git config --global user.email 'leynier41@gmail.com'
	git add docs/index.md
	git commit --allow-empty -m "Update docs/index.md"
	git push

run: install
	uv run uvicorn api.main:app --reload --host ${HOST} --port ${PORT}

build:
	docker build -t comohay-api:latest .

deploy:
	docker run -d -p 8000:80 --name comohay-api-container --env-file .env comohay-api:latest

rmcontainer:
	docker container rm comohay-api-container --force

rmimage:
	docker image rm comohay-api:latest

build_deploy: build deploy

rmall: rmcontainer rmimage

redeploy: rmall build_deploy
