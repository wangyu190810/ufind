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
    country = Column(Unicode(255))
    latitude = Column(Unicode(40), doc=u"经度")
    longitude = Column(Unicode(40), doc=u"纬度")
    offernum = Column(Integer)

    @classmethod
    def get_state_info(cls,connection):
        return connection.query(State)

    @classmethod
    def get_index(cls,connection,country):
        return connection.query(State).\
            filter(State.country == country)

    @classmethod
    def get_state_name(cls,connection,state_id):
        return connection.query(State).filter(State.id == state_id).scalar()