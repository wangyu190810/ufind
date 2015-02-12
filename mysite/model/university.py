# -*-coding:utf-8-*-
__author__ = ''
from sqlalchemy.schema import Table, Column
from sqlalchemy.types import Integer, Unicode, Float
from sqlalchemy.sql import select
from sqlalchemy.orm import aliased
from datetime import datetime

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
    menaGPA = Column(Unicode(255), doc=u"")
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
        if stateid == None:
            return connection.query(University).\
                filter(University.name.like("%"+searchname+"%"))
        else:
            return connection.query(University).\
                filter(University.name.like("%"+searchname+"%")).\
                filter(University.city == stateid)

    @classmethod
    def university_name_list(cls,connection):
        return connection.query(University.name)

    @classmethod
    def get_state_university(cls,connection,state_id):
        return connection.query(University).\
            filter(University.state_id == state_id)
