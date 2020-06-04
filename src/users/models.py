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
    uuid = Column(String(36), nullable=False, unique=True, default=str(uuid4()))
    name = Column(String(32), nullable=False)
    email = Column(String(64), nullable=True)
    phone = Column(String(32), nullable=True)
    password = Column(String(64), nullable=True)
    first_name = Column(String(32), nullable=True)
    last_name = Column(String(32), nullable=True)
    enabled = Column(Boolean, default=False)
