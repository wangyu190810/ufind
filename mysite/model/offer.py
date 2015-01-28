# -*-coding:utf-8-*-
__author__ = ''
from sqlalchemy.schema import Table, Column
from sqlalchemy.types import Integer, Unicode, Float
from sqlalchemy.sql import select

from time import time

from base import metadata, Base


class Offer(Base):
    __tablename__ = "offer"
    id = Column(Integer,primary_key=True,autoincrement=True)
    user_id = Column(Integer,doc=u"用户id")
    university_id = Column(Integer,doc=u"学校的id")
    major_id = Column(Integer,doc=u"专业id")
    result = Column(Integer,doc=u"状态位")
    create_time = Column(Integer,default=lambda: time())

    @classmethod
    def set_offer(cls,connection,user_id,university_id,major_id,result):
        offer = Offer(user_id=user_id,university_id=university_id,major_id=major_id,result=result)
        connection.add(offer)
        connection.commit()


