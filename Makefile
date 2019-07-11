.PHONY: test

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
	coverage run --source=users -m pytest test $(ARGS)

coverage: test coverage-report coverage-html


# docker
build-base:
	docker build --target base -t service-base .;
	docker build --target builder -t service-builder .;

build: build-base
	for image in $(IMAGES) ; do TAG=$(TAG) make -C $$image build-image; done

docker-save:
	mkdir -p docker-images
	docker save -o docker-images/services.tar $(foreach image, $(IMAGES), nameko/service-$(image):$(TAG))

docker-load:
	docker load -i docker-images/services.tar

docker-tag:
	for image in $(IMAGES) ; do make -C $$image docker-tag; done

docker-login:
	docker login --password=$(DOCKER_PASSWORD) --username=$(DOCKER_USERNAME)

push-images:
	for image in $(IMAGES) ; do make -C $$image push-image; done

