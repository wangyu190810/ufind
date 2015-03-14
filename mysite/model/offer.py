# -*-coding:utf-8-*-
__author__ = ''
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, Unicode
from sqlalchemy.sql import func

from time import time

from base import Base


class Offer(Base):
    __tablename__ = "offer"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, doc=u"用户id")
    university_id = Column(Integer, doc=u"学校的id")
    major_id = Column(Integer, doc=u"专业id")
    result = Column(Integer, doc=u"状态位")
    grade = Column(Unicode(80),doc=u"master硕士，pa博士")
    offer_type = Column(Unicode(80),doc=u"offer的类型，没有没有奖学金")
    scholarship = Column(Integer, doc=u"奖学金的数值")
    scholarship_type = Column(Unicode(80), doc=u"奖学金的类型")
    create_time = Column(Integer, default=lambda: time())

    @classmethod
    def set_offer(cls, connection, user_id,
                  university_id, major_id,
                  result, grade,
                  offer_type,
                  scholarship=None,
                  scholarship_type=None):
        offer = Offer(user_id=user_id, university_id=university_id,
                      major_id=major_id, result=result,
                      grade=grade,
                      offer_type=offer_type,
                      scholarship=scholarship,
                      scholarship_type=scholarship_type)
        connection.add(offer)
        connection.commit()

    @classmethod
    def get_offer_student(cls, connection, unviersity_id, major_id):
        """根据学校和专业随机的返回两个学生的id"""
        return connection.query(Offer). \
            filter(Offer.university_id == unviersity_id). \
            filter(Offer.major_id == major_id).limit(2)

    @classmethod
    def get_offer_student_info(cls, connection, student_id):
        """根据学生的id查看学生的offer"""
        return connection.query(Offer). \
            filter(Offer.user_id == student_id)

    @classmethod
    def get_offer_num(cls, connection, university_id):
        """查看当前学校的off数量"""
        return connection.query(func.count(Offer)). \
            filter(Offer.university_id == university_id).scalar()


    @classmethod
    def get_user_id_from_university(cls, connection, university_id,
                                    major_id=None):
        """根据学校找学生iD"""
        if major_id is None:
            return connection.query(Offer). \
                filter(Offer.university_id == university_id)
        return connection.query(Offer).filter(
            Offer.university_id == university_id). \
            filter(Offer.major_id == major_id)

    @classmethod
    def get_user_id_from_major(cls, connection, major_id):
        """根据专业id查找学生信息"""
        return connection.query(Offer).\
            filter(Offer.major_id == major_id).limit(2)

    @classmethod
    def get_site_offer_num(cls,connection):
        """全站offer数量"""
        return connection.query(func.count(Offer.id)).scalar()

    @classmethod
    def get_offer_num_from_major(cls,connection,university_id,major_id):
        return connection.query(func.count(Offer.id)).\
            filter(Offer.university_id == university_id).\
            filter(Offer.major_id == major_id).scalar()