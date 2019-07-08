# -*- coding: utf-8 -*-

from uuid import uuid4

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

from users.utils import utcnow


class ModelBase:

    created_at = Column(DateTime, nullable=False, default=utcnow)
    updated_at = Column(DateTime, nullable=False, default=utcnow, onupdate=utcnow)


DeclarativeBase = declarative_base(cls=ModelBase)


class Users(DeclarativeBase):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(64), nullable=True)
    phone = Column(String(32), nullable=True)
    password = Column(String(64), nullable=True)
    email_verified = Column(Boolean, nullable=False, default=False)
    uuid = Column(String(36), nullable=False, unique=True, default=str(uuid4()))
    enabled = Column(Boolean, nullable=False, default=False)
