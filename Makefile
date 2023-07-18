.venv:
	virtualenv .venv

tests: .venv
	.venv/bin/pip install -r requirements.txt -r requirements-test.txt
	.venv/bin/python -m pytest