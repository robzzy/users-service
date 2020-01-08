.PHONY: test

# vars
ifdef CIRCLE_SHA1
TAG ?= $(CIRCLE_SHA1)
else
TAG ?= $(shell git rev-parse HEAD)
endif

SERVICES := core
HTMLCOV_DIR ?= htmlcov
IMAGES := $(SERVICES) migrations

CONTEXT ?= david.k8s.local
NAMESPACE ?= demo
SERVICE_NAME ?= users-service
PROJECT_DOCKER_HOST ?= zengzhiyuan


install-dependencies:
	pip install -U -e ".[dev]"


# test
coverage-html:
	coverage html -d $(HTMLCOV_DIR) --fail-under 60 

coverage-report:
	coverage report -m

test:
	flake8 src test
	coverage run --concurrency=eventlet --source=users -m pytest test $(ARGS)

coverage: test coverage-report coverage-html


# docker
clean-source:
	docker rm source || true

docker-build-wheel: clean-source
	docker create -v /application -v /wheelhouse --name source alpine:3.4
	docker cp . source:/application
	docker run --rm --volumes-from source $(PROJECT_DOCKER_HOST)/python-builder:latest;
	docker cp source:/wheelhouse .
	docker rm source

build-base: docker-build-wheel
	docker pull $(PROJECT_DOCKER_HOST)/python-base:latest
	docker tag $(PROJECT_DOCKER_HOST)/python-base:latest python-base:latest
	docker build -t users-base .

build: build-base
	for image in $(IMAGES) ; do TAG=$(TAG) make -C deploy/$$image build-image; done

docker-login:
	echo $$DOCKER_PASSWORD | docker login --username=$(DOCKER_USERNAME) --password-stdin

docker-save:
	mkdir -p docker-images
	docker save -o docker-images/users-service.tar $(foreach image, $(IMAGES), users-service-$(image):$(TAG))

docker-load:
	docker load -i docker-images/users-service.tar

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
	--set image.tag=$(TAG) \
	--set run_migrations=$(RUN_MIGRATIONS) \
	--set db_revision=$(DB_REVISION);

lint-chart:
	helm lint deploy/k8s/charts/$(SERVICE_NAME) --strict

initial-cluster: deploy-namespace
	helm --kube-context=$(CONTEXT) install --name guest --namespace demo stable/rabbitmq
	helm --kube-context=$(CONTEXT) install --name root --namespace demo stable/mysql --set mysqlDatabase=users

