# coding: utf-8
# email: khahux@163.com

from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, Unicode

from .base import Base


class Faculty(Base):
    u"""学院"""
    __tablename__ = "faculty"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Unicode(255))
    chiname = Column(Unicode(255))
    university_id = Column(Integer)

    @classmethod
    def get_faculty_info(cls, connection, university_id=None):
        if university_id is None:
            return connection.query(Faculty).filter_by()
        else:
            return connection.query(Faculty).filter(Faculty.university_id
                                                    == university_id)