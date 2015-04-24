# -*-coding:utf-8-*-
__author__ = ''
from sqlalchemy.schema import Table, Column
from sqlalchemy.types import Integer, Unicode, Float
from sqlalchemy.sql import select
from sqlalchemy import func,text
from datetime import datetime

from base import metadata, Base

class Major(Base):
    """专业"""
    __tablename__ = "major"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Unicode(255),index=True)
    chiname = Column(Unicode(255))
    main_major = Column(Unicode(255))
    university_id = Column(Integer, index=True)
    faculty_id = Column(Integer, index=True)
    School2_ID = Column(Integer)
    School3_ID = Column(Integer)
    major_type = Column(Integer,doc=u"专业类型，1为本科生，2为研究生，3为博士生，0为不分级别")
    major_user_type = Column(Integer,doc=u"默认为零。用户填写的数据为1")
    introduction = Column(Unicode(225))


    @classmethod
    def add_major(cls,connection,name,main_major,university_id,faculty_id,
                  major_type,major_user_type=None):
        if major_user_type is None:
            major_user_type = 1
        else:
            major_user_type = 0
        major = Major(name=name,main_major=main_major,university_id=university_id,
                      faculty_id=faculty_id,major_type=major_type,major_user_type=major_user_type)
        connection.add(major)
        connection.commit()
        return connection.query(func.max(Major.id)).scalar()

    @classmethod
    def search_maior(cls, connection, searchname, university_id=None,major_type=None):
        if university_id is None:
           return connection.query(Major).\
               filter(Major.name.like("%"+searchname+"%"))
        elif university_id is not None and major_type is None:
            return connection.query(Major).\
                filter(Major.name.like("%"+searchname+"%")).\
                filter(Major.university_id == university_id)
        else:
           return connection.query(Major).\
               filter(Major.name.like("%"+searchname+"%")).\
               filter(Major.university_id == university_id).\
               filter(Major.major_type == major_type)

    @classmethod
    def get_major_info_university(cls,connection,university_id):
        return connection.query(Major).filter(
            Major.university_id == university_id
        )

    @classmethod
    def get_major_from_faculty(cls,connection,university_id,faculty_id):
        return connection.query(Major).filter(
            Major.university_id == university_id
        ).filter(Major.faculty_id == faculty_id)


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

    @classmethod
    def get_major_info_by_id_scalar(cls,connection,major_id):
        return connection.query(Major).filter(Major.id == major_id).scalar()


    @classmethod
    def get_major_exit(cls,connection,major_name):
        return connection.query(func.count(Major.id)).\
            filter(Major.name.like("%"+major_name+"%")).scalar()

