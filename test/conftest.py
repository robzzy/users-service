# -*- coding: utf-8 -*-

import os
import pytest

from users.models import Users, DeclarativeBase


@pytest.fixture(scope="session")
def model_base():
    return DeclarativeBase


@pytest.fixture(scope="session")
def db_url():
    return "mysql+mysqlconnector://%s:%s@%s/%s?charset=utf8" % (
        os.getenv("DB_USER", "root"),
        os.getenv("DB_PASS", ""),
        os.getenv("DB_SERVER", "localhost"),
        os.getenv("DB_NAME", "demo"),
    )


@pytest.fixture
def user():
    return {
        "id": 1,
        "email": "demo@test.com",
        "phone": "mock_phone",
        "password": "mock_password",
        "email_verified": False,
        "uuid": "mock_uuid",
        "enabled": False
    }


@pytest.fixture
def create_user(user, db_session):
    def create(**overrides):
        new_user = user.copy()
        new_user.update(**overrides)

        db_session.add(Users(**new_user))
        db_session.commit()

        return new_user
    return create
