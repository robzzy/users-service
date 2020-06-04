# -*- coding: utf-8 -*-

from marshmallow import Schema, fields


class UserSchema(Schema):

    name = fields.String(required=True, allow_none=False)
    email = fields.String(required=True, allow_none=True)
    phone = fields.String(required=True, allow_none=True)
    first_name = fields.String(required=True, allow_none=True)
    last_name = fields.String(required=True, allow_none=True)

    password = fields.String(required=True, allow_none=False, load_only=True)
