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

CONTEXT ?= david.k8s.local
NAMESPACE ?= demo
SERVICE_NAME ?= users-service


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
	echo $$DOCKER_PASSWORD | docker login --username=$(DOCKER_USERNAME) --password-stdin

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


# k8s

deploy-namespace:
	kubectl --context=$(CONTEXT) apply -f deploy/k8s/namespace.yaml


# helm

test-chart:
	helm upgrade users-service deploy/k8s/charts/$(SERVICE_NAME) --install \
	--namespace=$(NAMESPACE) --kube-context $(CONTEXT) \
	--dry-run --debug --set image.tag=$(TAG)

install-chart:
	helm upgrade users-service deploy/k8s/charts/$(SERVICE_NAME) --install \
	--namespace=$(NAMESPACE) --kube-context $(CONTEXT) \
	--set image.tage=$(TAG)

lint-chart:
	helm lint deploy/k8s/charts/$(SERVICE_NAME) --strict