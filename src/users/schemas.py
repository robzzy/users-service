# -*- coding: utf-8 -*-

from marshmallow import Schema, fields


class UserSchema(Schema):

    uuid = fields.String()
    email = fields.String()
    phone = fields.String()
    password = fields.String()
    email_verified = fields.Boolean(dump_only=True)
    enabled = fields.Boolean(dump_only=True)
