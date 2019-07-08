HTMLCOV_DIR ?= htmlcov
TAG ?= dev
IMAGES :=  users-service

install-dependencies:
	pip install -U -e ".[dev]"


# test
coverage-html:
	coverage html -d $(HTMLCOV_DIR) --fail-under 100

coverage-report:
	coverage report -m

test:
	flake8 src test
	coverage run -m pytest test $(ARGS)

coverage: test coverage-report coverage-html
