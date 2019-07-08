import pytest

from nameko.testing.services import worker_factory

from users.services.core.service import UsersService
from users.exceptions import UserNotFound
from users.models import Users
from users.schemas import UserSchema


@pytest.fixture
def users_service(db_session):
    service = worker_factory(UsersService, **{"db": db_session})
    return service


class TestUsersService:

    @pytest.fixture
    def created_user(self, create_user):
        return create_user()

    def test_health_check(self, users_service):

        response = users_service.health_check()

        assert response == '{"status": "succeeded"}'

    def test_get_user(self, users_service, created_user):

        _user = users_service.get_user(uuid="mock_uuid")
        _user.update({"id": 1, "uuid": "mock_uuid"})

        assert created_user == _user

    def test_get_use_when_user_not_found(self, users_service, created_user):

        with pytest.raises(UserNotFound):
            users_service.get_user(uuid="user_not_exists")

    def test_update_user(self, users_service, created_user, db_session):

        _user = users_service.update_user(
            1, {"email": "zzz@test.com"}
        )

        updated_user = db_session.query(Users).get(1)

        assert _user == UserSchema().dump(updated_user).data

    def test_update_user_not_found(self, users_service):

        with pytest.raises(UserNotFound):
            users_service.update_user(1, {"uuid": "mock_uuid"})

    def test_create_user(self, users_service, db_session, create_user):

        create_user()

        assert len(db_session.query(Users).all()) == 1

    def test_delete_user(self, users_service, created_user, db_session):

        assert len(db_session.query(Users).all()) == 1

        users_service.delete_user(1)

        assert len(db_session.query(Users).all()) == 0
