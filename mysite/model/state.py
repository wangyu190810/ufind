# -*-coding:utf-8-*-
__author__ = ''
from sqlalchemy.schema import Table, Column
from sqlalchemy.types import Integer, Unicode, Float
from sqlalchemy.sql import select

from datetime import datetime

from base import metadata, Base


class State(Base):
    """地区"""
    __tablename__ = "state"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Unicode(255))
    offernum = Column(Integer)

