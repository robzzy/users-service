
import pytest
from mock import call, patch
from nameko.testing.services import worker_factory

from users.services.core.service import UsersService
from users.exceptions import UserNotFound
from users.models import Users
from users.schemas import UserSchema
from users.dependencies.auth import InvalidToken


@pytest.fixture
def users_service(db_session):
    service = worker_factory(UsersService, **{"db": db_session})
    return service


class TestUsersService:

    @pytest.fixture
    def created_user(self, create_user):
        return create_user()

    def test_health_check(self, users_service):

        response = users_service.health_check("request")

        assert response == '{"status": "ok"}'

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
        assert users_service.event_dispatcher.call_args == call(
            "user_updated", {
                "uuid": "mock_uuid",
                "data": {
                    "email": "zzz@test.com",
                }
            }
        )

    def test_update_user_not_found(self, users_service):

        with pytest.raises(UserNotFound):
            users_service.update_user(1, {"uuid": "mock_uuid"})

    def test_create_user(self, users_service, db_session):

        user_data = {"email": "1", "password": 1, "phone": "1"}

        with patch("users.services.core.service.uuid4") as uuid4:
            uuid4.return_value = "mock_uuid"
            users_service.create_user(data=user_data)

        assert len(db_session.query(Users).all()) == 1
        assert users_service.event_dispatcher.call_args == call(
            "user_created", {
                "data": {
                    "email": "1",
                    "password": 1,
                    "phone": "1",
                    "uuid": "mock_uuid",
                }
            }
        )

    def test_delete_user(self, users_service, created_user, db_session):

        assert len(db_session.query(Users).all()) == 1

        users_service.delete_user(1)

        assert len(db_session.query(Users).all()) == 0
        assert users_service.event_dispatcher.call_args == call(
            "user_deleted", {"uuid": "mock_uuid"}
        )

    def test_list_users(self, users_service, db_session):

        user_1 = {
            "email": "demo1@test.com",
            "phone": "mock_phone",
            "password": "mock_password",
            "email_verified": False,
            "uuid": "mock_uuid",
            "enabled": False
            }
        user_2 = user_1.copy()
        user_2.update({"uuid": "2", "email": "demo2@test.com"})

        db_session.add(Users(**user_1))
        db_session.add(Users(**user_2))
        db_session.commit()

        users = users_service.list_users(
            filters={"field": "phone", "op": "==", "value": "mock_phone"},
            order_by={"field": "id", "direction": "desc"},
            offset="0",
            limit=10,
        )

        assert users == [
            {
                "uuid": "2",
                "email": "demo2@test.com",
                "phone": "mock_phone",
                "password": "mock_password",
                "email_verified": False,
                "enabled": False
            },
            {
                "uuid": "mock_uuid",
                "email": "demo1@test.com",
                "phone": "mock_phone",
                "password": "mock_password",
                "email_verified": False,
                "enabled": False
            }
        ]

    def test_check_jwt(self, users_service, created_user):

        users_service.auth.decode_jwt.return_value = {
            "uuid": "mock_uuid",
        }
        users_service.auth.encode_jwt.return_value = "token"

        token = users_service.check_jwt()

        assert token == "token"

    def test_check_jwt_raise_invalid_token(self, users_service):
        users_service.auth.decode_jwt.side_effect = InvalidToken()

        token = users_service.check_jwt()

        assert not token

    def test_check_jwt_user_not_found(self, users_service):
        users_service.auth.decode_jwt.return_value = {
            "uuid": "mock_uuid",
        }

        token = users_service.check_jwt()

        assert not token
