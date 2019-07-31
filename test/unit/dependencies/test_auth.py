# -*- coding: utf-8 -*-


import pytest
from mock import patch
from nameko import config
from nameko.exceptions import ConfigurationError
from jwt.exceptions import InvalidKeyError, InvalidTokenError, DecodeError

from users.dependencies.auth import Auth, NoToken, InvalidToken


class TestAuth:

    @pytest.fixture
    def auth_dependency(self, mock_container):
        return Auth().bind(mock_container, "auth")

    @pytest.fixture
    @config.patch({"JWT_SECRET": "jwt_secret"})
    def provider_dependency(self, auth_dependency):
        auth_dependency.setup()

        worker_cxt = type(
            "worker", (), {
                "data": {
                    "authorization": {
                        "schema": "Bearer",
                        "param": "token"
                    }
                }
            })
        dependency_provider = auth_dependency.get_dependency(worker_cxt)
        return dependency_provider

    @config.patch({"JWT_SECRET": None})
    def test_config_not_found(self, auth_dependency):

        with pytest.raises(ConfigurationError):
            auth_dependency.setup()

    def test_get_auth_dependency(self, provider_dependency):

        assert isinstance(provider_dependency, Auth.AuthWrapper)

    def test_auth_encode_jwt(self, provider_dependency):

        with patch("users.dependencies.auth.jwt") as _jwt:

            _jwt.encode.return_value = b"jwt_token"

            token = provider_dependency.encode_jwt({"uuid": "uuid1"})

        assert token == "jwt_token"

    def test_auth_decode_jwt(self, provider_dependency):

        with patch("users.dependencies.auth.jwt") as _jwt:

            _jwt.decode.return_value = {"uuid": "uuid1"}

            payload = provider_dependency.decode_jwt()

        assert payload == {"uuid": "uuid1"}

    @config.patch({"JWT_SECRET": "jwt_secret"})
    def test_auth_decode_jwt_without_self_jwt(self, auth_dependency):
        auth_dependency.setup()
        worker_cxt = type(
            "worker", (), {
                "data": {
                    "authorization": {
                        "schema": "Bearer",
                        "param": None
                    }
                }
            })
        dependency_provider = auth_dependency.get_dependency(worker_cxt)

        with pytest.raises(NoToken):
            dependency_provider.decode_jwt()

    @pytest.mark.parametrize(
        "jwt_error",
        (
            DecodeError,
            InvalidKeyError,
            InvalidTokenError,
        )
    )
    def test_auth_decode_jwt_with_jwt_error(self, provider_dependency, jwt_error):

        with patch("users.dependencies.auth.jwt") as _jwt:
            _jwt.decode.side_effect = jwt_error

            with pytest.raises(InvalidToken):
                provider_dependency.decode_jwt()

    @pytest.mark.parametrize(
        "payload, call_args",
        (
            (
                {"email": "email1", "uuid": None},
                ("email2", None),
            ),
            (
                {"email": None, "uuid": "uuid1"},
                (None, "uuid2"),
            ),
        )
    )
    def test_auth_raise_unauthorised_error(
        self, provider_dependency, payload, call_args
    ):
        with patch("users.dependencies.auth.jwt") as _jwt:
            _jwt.decode.return_value = payload

            with pytest.raises(InvalidToken):
                provider_dependency.decode_jwt(*call_args)
