HTMLCOV_DIR ?= htmlcov
TAG ?= dev
IMAGES :=  users-service

install-dependencies:
	pip install -U -e "users-service/.[dev]"


# test
coverage-html:
	coverage html -d $(HTMLCOV_DIR) --fail-under 100

coverage-report:
	coverage report -m

test:
	flake8 users-service/src users-service/test
	coverage run -m pytest users-service $(ARGS)

coverage: test coverage-report coverage-html


