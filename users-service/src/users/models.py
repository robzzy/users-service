# -*- coding: utf-8 -*-


from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ModelBase(Base):
    pass
