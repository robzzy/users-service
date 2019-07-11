
.PHONY: etc

COMPONENT := core


include ../Makefile.common


run:
	nameko run --config config.yaml users.services.$(COMPONENT).service:UsersService



build-image:
	docker build -t users-service:$(TAG) .;

docker-tag:
	docker tag users-service:$(FROM_TAG) users-service:$(TAG)

push-image:
	docker push users-service:$(TAG)

