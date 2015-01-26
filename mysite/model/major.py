# -*-coding:utf-8-*-
__author__ = ''
from sqlalchemy.schema import Table, Column
from sqlalchemy.types import Integer, Unicode, Float
from sqlalchemy.sql import select

from datetime import datetime

from base import metadata, Base

class Major(Base):
    """专业"""
    __tablename__ = "major"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Unicode(255))
    chiname = Column(Unicode(255))
    university_id = Column(Unicode(225))
    faculty_id = Column(Unicode(225))
    introduction = Column(Unicode(225))


    @classmethod
    def search_maior(cls, connection, searchname, university_id=None):
        if university_id is None:
           return connection.query(Major).\
               filter(Major.name.like("%"+searchname+"%"))
        else:
           return connection.query(Major).\
               filter(Major.name.like("%"+searchname+"%")).\
               filter(Major.university_id == university_id)


    @classmethod
    def get_major_info(cls, connection, university_id, faculty_id):
        return connection.query(Major).\
            filter(Major.university_id == university_id).\
            filter(Major.faculty_id == faculty_id)

