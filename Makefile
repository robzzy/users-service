HTMLCOV_DIR ?= htmlcov
TAG ?= dev
IMAGES :=  users-service

install-dependencies:
	pip install -U -e ".[dev]"


# test
coverage-html: test
	coverage html -d $(HTMLCOV_DIR) --fail-under 100

coverage-report: test
	coverage report -m

test:
	flake8 src test
	coverage run --source=users -m pytest test $(ARGS)

coverage: test coverage-report coverage-html
