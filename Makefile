.venv:
	python3 -m pip install poetry
	python3 -m poetry install

tests: .venv
	AUTHENTIK_USER_PATH='test' HACKSPACE_DOORS_ALLOWED_GROUP='Public' AUTHENTIK_TOKEN='xxx' HOMEASSISTANT_TOKEN='xxx' python3 -m poetry run pytest

update-cassettes: .venv
	AUTHENTIK_USER_PATH='test' HACKSPACE_DOORS_ALLOWED_GROUP='Public' python3 -m poetry run pytest

lint: .venv
	python3 -m poetry run ruff --format=github --select=E9,F63,F7,F82 --target-version=py37 .
	python3 -m poetry run ruff --format=github --target-version=py37 .

serve:
	python3 -m poetry run uvicorn hackspaceapi.main:app --reload
