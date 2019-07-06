import json

from nameko.rpc import rpc
from nameko_sqlalchemy import DatabaseSession
from users.models import DeclarativeBase


class UsersService:

    name = "users"

    db = DatabaseSession(DeclarativeBase)

    @rpc
    def health_check(self):
        return json.dumps({
            "status": "succeeded"
        })
