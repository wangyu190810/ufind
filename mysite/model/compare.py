# -*-coding: utf-8-*-

__author__ = 'wangyu'

from time import time

from sqlalchemy import func
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, Unicode

from mysite.model.base import Base


class CompareInfo(Base):
    """投票的具体信息"""
    __tablename__ = "compareinfo"
    id = Column(Integer, primary_key=True, autoincrement=True)
    university_id = Column(Integer, doc=u"大学的id")
    major_id = Column(Integer, doc=u"专业id")
    compare_id = Column(Integer, doc=u"发起id")
    supportnum = Column(Integer,doc=u"支持个数")


    @classmethod
    def set_compare_info(cls,connection, university_id, major_id, compare_id):
        compare_info = CompareInfo(university_id=university_id,major_id=major_id,compare_id=compare_id)
        connection.add(compare_info)
        connection.commit()

    @classmethod
    def get_compare_info(cls,connection,compare_id):
        return connection.query(CompareInfo).\
            filter(CompareInfo.compare_id == compare_id)

    @classmethod
    def get_compare_random(cls,connection,university_id,major_id):
        return connection.query(CompareInfo.compare_id).\
            filter(CompareInfo.university_id == university_id).\
            filter(CompareInfo.major_id == major_id).\
            order_by(func.random()).limit(2)

    @classmethod
    def get_compare_about_major(cls,connection,major_id):
        return connection.query(CompareInfo).\
            filter(CompareInfo.major_id==major_id)

    @classmethod
    def get_compare_university_major(cls,connection,university_id,
                                     major_id=None):
        if major_id is None:
            return connection.query(CompareInfo).\
                filter(CompareInfo.university_id == university_id)
        return connection.query(CompareInfo).\
            filter(CompareInfo.university_id == university_id).\
            filter(CompareInfo.major_id == major_id)


class Compare(Base):
    """投票信息"""
    __tablename__ = "compare"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, doc=u"发起投票的用户id")
    description = Column(Unicode(255), doc=u"发起投票的描述")
    create_time = Column(Integer, default=lambda: time(), doc=u"投票发起时间")

    @classmethod
    def set_compare(cls, connection, user_id, description):
        compare = Compare(user_id=user_id,description=description)
        connection.add(compare)
        connection.commit()

    @classmethod
    def get_compare_id(cls, connection):
        return connection.query(func.max(Compare.id)).as_scalar()


    @classmethod
    def get_compare(cls,connection,compaer_id):
        return connection.query(Compare).filter(Compare.id == compaer_id).scalar()

    @classmethod
    def get_compare_user_id(cls,connection,user_id):
        """用户的id获取用户发起国的投票"""
        return connection.query(Compare).filter(Compare.user_id == user_id)


class CompareSupport(Base):
    __tablename__ = "comparesupport"
    id = Column(Integer,primary_key=True,autoincrement=True)
    user_id = Column(Integer,doc=u"投票用户的id")
    compare_id = Column(Integer,doc=u"投向哪个投票列表")
    compare_info_id = Column(Integer,doc=u"投票的具体投向哪个")
    create_time = Column(Integer,default=lambda: time(),doc=u"创建时间")

    @classmethod
    def set_compare_support(cls,connection,user_id,compare_info_id):
        compare_info = connection.query(CompareInfo).\
            filter(CompareInfo.id == compare_info_id).scalar()
        compare_support = CompareSupport(user_id=user_id,
                                         compare_id=compare_info.compare_id,
                                         compare_info_id=compare_info.id)
        connection.add(compare_support)

        count = connection.query(func.count(CompareSupport.compare_info_id)).\
            filter(CompareSupport.compare_info_id == compare_info_id).scalar()

        connection.query(CompareInfo).\
            filter(CompareInfo.id == compare_info_id).\
            update({"supportnum":count+1})
        connection.commit()



