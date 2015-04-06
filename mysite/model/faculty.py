# -*-coding:utf-8-*-
__author__ = ''
from sqlalchemy.schema import Table, Column
from sqlalchemy.types import Integer, Unicode, Float
from sqlalchemy.sql import select

from base import Base
from datetime import datetime


class Faculty(Base):
    """学院"""
    __tablename__ = "faculty"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Unicode(255))
    chiname = Column(Unicode(255))
    university_id = Column(Integer)

    # @classmethod
    # def get_faculty_info(cls, connection, university_id=None):
    #     if university_id is None:
    #         return connection.query(Faculty).filter_by()
    #     else:
    #         return connection.query(Faculty).filter(Faculty.university_id
    #                                                 == university_id)
    #
    #
    @classmethod
    def get_faculty_info(cls, connection, university_id=None):
        return connection.query(Faculty).limit(6)




