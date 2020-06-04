import json

from nameko.rpc import rpc
from nameko.events import EventDispatcher
from nameko_tracer import Tracer
from nameko_sqlalchemy import DatabaseSession
from nameko.web.handlers import http

from users.models import DeclarativeBase
from users.exceptions import UserNotFound
from users.dependencies.auth import Auth, InvalidToken
from users.services.core.users import UserMixin


class UsersService(UserMixin):

    name = "users"

    auth = Auth()
    tracer = Tracer()
    db_session = DatabaseSession(DeclarativeBase)
    event_dispatcher = EventDispatcher()

    @http("GET", "/healthcheck")
    def health_check_http(self, request):
        return json.dumps(self.health_check())

    @rpc
    def health_check(self):
        result = {"status": "ok"}
        return result

    @rpc
    def check_jwt(self):

        try:
            decoded_jwt = self.auth.decode_jwt()
        except InvalidToken:
            return None

        try:
            user = self.get_user(uuid=decoded_jwt["uuid"])
        except UserNotFound:
            return None

        return self.auth.encode_jwt({
            "uuid": user["uuid"],
            "email": user["email"]
        })
