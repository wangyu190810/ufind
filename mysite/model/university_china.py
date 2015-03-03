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


class SeniorHighSchool(Base):
    """国内高中"""
    __tablename__ = "senior_high"
    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(Unicode(255))
    location = Column(Unicode(255))
    Province = Column(Unicode(255))
    city = Column(Unicode(255))
    district = Column(Unicode(255))


class MajorChina(Base):
    """国内大学专业"""
    __tablename__ = "major_china"
    id = Column(Integer,primary_key=True,autoincrement=True)
    faculty_id = Column(Integer)
    faculty_name = Column(Unicode(255))
    major_id = Column(Integer)
    major_name = Column(Unicode(255))

