.PHONY: etc

COMPONENT := core


include ../Makefile.common


run:
	nameko run --config config.yaml users.services.$(COMPONENT).service:UsersService

