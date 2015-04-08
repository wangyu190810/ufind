# -*-coding:utf-8-*-
__author__ = ''
from sqlalchemy.schema import Table, Column
from sqlalchemy.types import Integer, Unicode, Float
from sqlalchemy.sql import select
from sqlalchemy.orm import aliased
from datetime import datetime
from sqlalchemy import or_
from base import Base


class University(Base):
    """学校"""
    __tablename__ = "university"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Unicode(255))
    chiname = Column(Unicode(255))
    short_name = Column(Unicode(255), doc=u"大学缩写")
    rank = Column(Integer,doc=u"排名")
    schoollogo = Column(Unicode(255), doc=u"学校图标")
    official = Column(Unicode(1000), doc=u"学校的官网地址")
    baidu = Column(Unicode(1000), doc=u"百度介绍")
    wiki = Column(Unicode(1000), doc=u"wiki介绍")
    menaGPA_Total = Column(Integer, doc=u"")
    menaGPA_0 = Column(Integer, doc=u"")
    menaGPA_1 = Column(Integer, doc=u"")
    menaTOEFL = Column(Integer, doc=u"")
    menaIELTS = Column(Integer, doc=u"")
    latitude = Column(Unicode(40), doc=u"经度")
    longitude = Column(Unicode(40), doc=u"纬度")
    country = Column(Unicode(255))
    state_id = Column(Integer, doc=u"地区id")
    city = Column(Unicode(255))


    @classmethod
    def get_university_info(cls, connection, university_id=None):
        if university_id is None:
            return connection.query(University)
            #return connection.query(University).all()
            #return connection.execute(stmt)

        else:
            return connection.query(University).filter(University.id
                                                       == university_id)

    @classmethod
    def search_university(cls, connection, searchname=None, stateid=None):
        if stateid is None:
            return connection.query(University).\
                filter(or_(University.name.like("%"+searchname+"%"),
                           University.short_name == searchname)).limit(10)
        else:
            return connection.query(University).\
                filter(or_(University.name.like("%"+searchname+"%"),
                           University.short_name == searchname)).\
                filter(University.state_id == stateid).limit(10)

    @classmethod
    def university_name_list(cls, connection):
        return connection.query(University.name).\
            filter(University.latitude is None)

    @classmethod
    def get_state_university(cls, connection, state_id):
        return connection.query(University).\
            filter(University.state_id == state_id)

    @classmethod
    def get_university_from_id(cls, connection, university_id):
        return connection.query(University).\
            filter(University.id == university_id).scalar()

    @classmethod
    def set_GPA_TOEFL_IELTS(cls,connection,university_id,GPA,GPA_0,GPA_1,TOEFL,IELTS):
        connection.query(University).filter(University.id == university_id).update(
            {
                University.menaGPA_Total: GPA,
                University.menaGPA_0: GPA_0,
                University.menaGPA_1: GPA_1,
                University.menaTOEFL: TOEFL,
                University.menaIELTS: IELTS
            }
        )
        connection.commit()
