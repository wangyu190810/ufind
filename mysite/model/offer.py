# -*-coding:utf-8-*-
__author__ = ''
from sqlalchemy.schema import Table, Column
from sqlalchemy.types import Integer, Unicode, Float
from sqlalchemy.sql import select,func

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


    @classmethod
    def get_offer_student(cls,connection,unviersity_id,major_id):
        """根据学校和专业随机的返回两个学生的id"""
        return connection.query(func.random(Offer.user_id)).\
            filter(Offer.university_id == unviersity_id).\
            filter(Offer.major_id == major_id).limit(2)

    @classmethod
    def get_offer_student_info(cls,connection,student_id):
        """根据学生的id查看学生的offer"""
        return connection.query(Offer).\
            filter(Offer.user_id == student_id)

    @classmethod
    def get_offer_num(cls,connection,university_id):
        """查看当前学校的off数量"""
        return connection.query(func.count(Offer)).\
            filter(Offer.university_id == university_id).scalar()


    @classmethod
    def get_user_id_from_university(cls,connection,university_id):
        """根据学校找学生iD"""
        return connection.query(Offer).\
            filter(Offer.university_id == university_id)
