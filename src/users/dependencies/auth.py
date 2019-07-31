# -*- coding: utf-8 -*-

from datetime import datetime

import jwt
from nameko import config
from nameko.exceptions import ConfigurationError
from nameko.extensions import DependencyProvider
from jwt.exceptions import InvalidKeyError, InvalidTokenError, DecodeError


JWT_KEY = "Auth"


class InvalidToken(Exception):
    pass


class NoToken(Exception):
    pass


class Auth(DependencyProvider):

    class AuthWrapper:

        def __init__(self, secret, worker_ctx):
            self.secret = secret
            self.worker_ctx = worker_ctx

            auth = self.worker_ctx.data.get("authorization")

            if auth and auth["schema"].lower() == "bearer":
                self.jwt = auth["param"]

        def encode_jwt(self, payload, algorithm="HS256"):

            payload["iat"] = datetime.utcnow()
            payload["iss"] = JWT_KEY

            self.jwt = jwt.encode(
                payload, self.secret, algorithm
            ).decode("utf-8")

            self.worker_ctx.data["authorization"] = {
                "schema": "bearer",
                "param": self.jwt
            }

            return self.jwt

        def decode_jwt(self, email=None, uuid=None, algorithm="HS256"):

            if not self.jwt:
                raise NoToken("Token not found.")

            try:
                payload = jwt.decode(
                    self.jwt, self.secret, algorithms=algorithm, issuer=JWT_KEY
                )
            except (
                DecodeError,
                InvalidTokenError,
                InvalidKeyError,
            ):
                raise InvalidToken(f"Token{self.jwt} is invalid.")

            if email and email != payload.get("email"):
                raise InvalidToken("Unauthorised user.")

            if uuid and uuid != payload.get("uuid"):
                raise InvalidToken("Unauthorised user.")

            return payload

    def setup(self):
        secret = config.get("JWT_SECRET")
        if not secret:
            raise ConfigurationError("Not found `JWT_SECRET`.")
        self.secret = secret

    def get_dependency(self, worker_ctx):
        return Auth.AuthWrapper(self.secret, worker_ctx)
