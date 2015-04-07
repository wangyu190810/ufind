# coding: utf-8
# email: khahux@163.com

from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, Unicode

from models.base import Base


class Faculty(Base):
    u"""学院"""
    __tablename__ = "faculty"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Unicode(255))
    chiname = Column(Unicode(255))
    university_id = Column(Integer)

    @classmethod
    def get_faculty_info(cls, connection, university_id=None):

        return connection.query(Faculty).limit(6)


