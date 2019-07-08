import json

from nameko.rpc import rpc
from nameko_tracer import Tracer
from nameko_sqlalchemy import DatabaseSession

from users.models import DeclarativeBase, Users
from users.schemas import UserSchema
from users.exceptions import UserNotFound


class UsersService:

    name = "users"

    tracer = Tracer()
    db = DatabaseSession(DeclarativeBase)

    @rpc
    def health_check(self):
        return json.dumps({
            "status": "succeeded"
        })

    @rpc(expected_exceptions=(UserNotFound,))
    def get_user(self, uuid):
        query = self.db.query(Users)

        user = query.filter(Users.uuid == uuid).first()

        if not user:
            raise UserNotFound(f"User do not exists.")

        return UserSchema().dump(user).data

    @rpc(expected_exceptions=(UserNotFound,))
    def update_user(self, id_, data):

        user_data = UserSchema(strict=True).load(data).data

        user = self.db.query(Users).get(id_)

        if not user:
            raise UserNotFound()

        for key, value in user_data.items():
            setattr(user, key, value)

        self.db.commit()

        return UserSchema().dump(user).data

    @rpc
    def create_user(self, data):

        user_data = UserSchema().load(data).data

        user = Users(**user_data)

        self.db.add(user)
        self.db.commit()

        return UserSchema().dump(user).data

    @rpc
    def delete_user(self, id_):

        user = self.db.query(Users).get(id_)

        self.db.delete(user)
        self.db.commit()
