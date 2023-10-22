.venv:
	python3 -m pip install poetry
	python3 -m poetry install --with test,github

.PHONY: tests
tests: .venv
	HOMEASSISTANT_TOKEN='xxx' python3 -m poetry run pytest

update-cassettes: .venv
	python3 -m poetry run pytest

lint: .venv
	python3 -m poetry run ruff --output-format=github --select=E9,F63,F7,F82 --target-version=py37 .
	python3 -m poetry run ruff --output-format=github --target-version=py37 .

serve:
	python3 -m poetry run uvicorn hackspaceapi.main:app --reload

gen-settings:
	PYTHONPATH="$PYTHONPATH:." HOMEASSISTANT_TOKEN='xxx' python3 tools/extract_settings.py