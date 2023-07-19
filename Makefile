.venv:
	python3 -m pip install poetry
	python3 -m poetry install

tests: .venv
	HOMEASSISTANT_TOKEN='xxx' python3 -m poetry run pytest

lint: .venv
	python3 -m poetry run ruff --format=github --select=E9,F63,F7,F82 --target-version=py37 .
	python3 -m poetry run ruff --format=github --target-version=py37 .