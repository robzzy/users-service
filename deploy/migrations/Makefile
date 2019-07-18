.PHONY: etc

COMPONENT := migrations
REVISION ?= head


include ../Makefile.common

migrate:
	alembic upgrade $(REVISION) || alembic downgrade $(REVISION)
