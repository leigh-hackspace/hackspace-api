.venv:
	python3 -m pip install poetry
	python3 -m poetry install

tests: .venv
	HOMEASSISTANT_TOKEN='xxx' python3 -m poetry run pytest