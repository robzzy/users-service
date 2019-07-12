.PHONY: test

# vars
ifdef CIRCLE_SHA1
TAG ?= $(CIRCLE_SHA1)
else
TAG ?= $(shell git rev-parse HEAD)
endif

SERVICES := core
HTMLCOV_DIR ?= htmlcov
IMAGES :=  $(SERVICES)

install-dependencies:
	pip install -U -e ".[dev]"


# test
coverage-html:
	coverage html -d $(HTMLCOV_DIR) --fail-under 100

coverage-report:
	coverage report -m

test:
	flake8 src test
	coverage run --source=users -m pytest test $(ARGS)

coverage: test coverage-report coverage-html


# docker

docker-login:
	docker login --password=$(DOCKER_PASSWORD) --username=$(DOCKER_USERNAME)

build-base:
	docker build --target base -t service-base .;
	docker build --target builder -t service-builder .;

build: build-base
	for image in $(IMAGES) ; do TAG=$(TAG) make -C deploy/$$image build-image; done

docker-save:
	mkdir -p docker-images
	docker save -o docker-images/users-services.tar $(foreach image, $(IMAGES), users-service-$(image):$(TAG))

docker-load:
	docker load -i docker-images/users-services.tar

docker-tag:
	for image in $(IMAGES) ; do make -C deploy/$$image docker-tag; done

push-images:
	for image in $(IMAGES) ; do make -C deploy/$$image docker-push; done

