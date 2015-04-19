# -*-coding:utf-8-*-
__author__ = ''
from sqlalchemy.schema import Table, Column
from sqlalchemy.types import Integer, Unicode, Float
from sqlalchemy.sql import select

from datetime import datetime

from base import metadata, Base


class MajorKye(Base):
    """专业"""
    __tablename__ = "major_key"
    Main_Major = Column(Unicode(255))
    Key_Word = Column(Unicode(255),primary_key=True)

    @classmethod
    def get_main_major(cls,connection,key):
        return connection.query(MajorKye).filter(MajorKye.Key_Word.like("%"+key+"%")).scalar()

