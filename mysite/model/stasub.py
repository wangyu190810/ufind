# -*-coding:utf-8-*-
__author__ = 'wangyu'
from sqlalchemy import Column, String, TEXT, Integer, Unicode, Float
from base import Base

class Stasub(Base):
    __tablename__ = "sub"
    id = Column(Integer, primary_key=True, autoincrement=True)
    sub_id = Column(Integer)
    grade = Column(Integer, default=0, doc=u"级别")
    sub_type = Column(Integer,doc=u"sub的类型属于GRE，还是属于STA")
    user_id = Column(Integer)

    @classmethod
    def set_sub(cls,connection,sub_id,grade,sub_type,user_id):
        stasub = Stasub(sub_id=sub_id, grade=grade,
                        sub_type=sub_type, user_id=user_id)
        connection.add(stasub)
        connection.commit()

    @classmethod
    def del_sub(cls,connection,user_id):
        u"""删除sub"""
        return connection.query(Stasub).filter(Stasub.user_id==user_id).delete()

    @classmethod
    def get_sub(cls,connection,user_id):
        u"""获取sub"""
        return connection.query(Stasub).filter(Stasub.user_id == user_id)



class SubContent(Base):
    __tablename__ = "subcontent"
    id = Column(Integer,primary_key=True,autoincrement=True)
    content = Column(Unicode(255))
    sub_type = Column(Integer)

    @classmethod
    def set_sub_content(cls,connection,content,sub_type):
        subcontent = SubContent(content=content,sub_type=sub_type)
        connection.add(subcontent)
        connection.commit()

    @classmethod
    def get_sub_content(cls,connection,sub_type):
        return connection.query(SubContent).filter(SubContent.sub_type==sub_type)



