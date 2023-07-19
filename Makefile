.venv:
	poetry install

tests: .venv
	HOMEASSISTANT_TOKEN='xxx' poetry run pytest