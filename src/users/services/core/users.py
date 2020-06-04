# -*- coding: utf-8 -*-

from nameko_autocrud import AutoCrud

from users.models import Users
from users.schemas import UserSchema


class UserMixin:

    users_autocrud = AutoCrud(
        "db_session",
        model_cls=Users,
        get_method_name="get_user",
        create_method_name="create_user",
        update_method_name="update_user",
        list_method_name="list_users",
        count_method_name="count_users",
        from_serializable=lambda obj: UserSchema().load(obj).data,
        to_serializable=lambda obj: UserSchema(strict=True).dump(obj).data,
    )
