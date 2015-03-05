# -*-coding:utf-8-*-
__author__ = 'Administrator'
from sqlalchemy.schema import Table, Column
from sqlalchemy.types import Integer, Unicode, Float
from sqlalchemy.sql import select
from sqlalchemy.orm import aliased
from datetime import datetime
from sqlalchemy import or_
from base import Base


class UniversityChina(Base):
    """国内大学"""
    __tablename__ = "university_china"
    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(Unicode(255))
    location = Column(Unicode(255))

    @classmethod
    def get_university_china_info(cls,connection,university_id):
        """国内大学的信息"""
        return connection.query(UniversityChina).\
            filter(UniversityChina.id == university_id).scalar()

    @classmethod
    def search_university_china(cls,connection,name):
        """搜索国内大学的名字"""
        return connection.query(UniversityChina).\
            filter(UniversityChina.name == name).limit(10)

class SeniorHighSchool(Base):
    """国内高中"""
    __tablename__ = "senior_high"
    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(Unicode(255))
    location = Column(Unicode(255))
    Province = Column(Unicode(255))
    city = Column(Unicode(255))
    district = Column(Unicode(255))

    @classmethod
    def get_senior_high(cls,connection, senior_id):
        return connection.query(SeniorHighSchool).\
            filter(SeniorHighSchool.id == senior_id).scalar()


    @classmethod
    def search_senior_high(cls,connection,name=None,city=None):
        """按照大学高中名字和高中地区搜学校"""
        return connection.query(SeniorHighSchool).\
            filter(or_(
                SeniorHighSchool.name.like("%"+name+"%"),
                SeniorHighSchool.city.like("%"+city+"%"))).\
            limit(10)

class MajorChina(Base):
    """国内大学专业"""
    __tablename__ = "major_china"
    id = Column(Integer,primary_key=True,autoincrement=True)
    faculty_id = Column(Integer)
    faculty_name = Column(Unicode(255))
    major_id = Column(Integer)
    major_name = Column(Unicode(255))

    @classmethod
    def get_major_china(cls,connection,id):
        """获取国内大学专业信息"""
        return connection.query(MajorChina).filter(MajorChina.id == id).scalar()

    @classmethod
    def search_major_china(cls,connection,faculty_name,major_name):
        return connection.query(MajorChina).\
            filter(or_(
                MajorChina.faculty_name.like("%"+faculty_name+"%"),
                MajorChina.major_name.like("%"+major_name+"%"))).limit(10)


