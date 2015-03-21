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
    main_major = Column(Unicode(255))
    university_id = Column(Integer)
    faculty_id = Column(Integer)
    major_type = Column(Integer,doc=u"专业类型，1为本科生，2为研究生，3为博士生，0为不分级别")
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
    def get_major_info_university(cls,connection,university_id):
        return connection.query(Major).filter(
            Major.university_id == university_id
        )

    @classmethod
    def get_major_from_faculty(cls,connection,university_id,faculty_id):
        return connection.query(Major).filter(
            Major.university_id == university_id
        ).filter(
            Major.faculty_id == faculty_id
        )


    @classmethod
    def get_major_info(cls, connection, university_id, faculty_id=None,major_id=None):
        if major_id is None:

            return connection.query(Major).\
                filter(Major.university_id == university_id).\
                filter(Major.faculty_id == faculty_id)
        else:
            return connection.query(Major).\
                filter(Major.id == major_id).\
                filter(Major.university_id == university_id)

    @classmethod
    def get_major_by_name(cls,connection,major_name,major_id):
        return connection.query(Major).\
            filter(Major.name == major_name).\
            filter(Major.id != major_id)


    @classmethod
    def get_major_info_by_id(cls,connection,major_id):
        return connection.query(Major).filter(Major.id == major_id)