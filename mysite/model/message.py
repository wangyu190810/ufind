# -*-coding: utf-8-*-

__author__ = 'wangyu'

from time import time

from sqlalchemy import Column, Integer, TEXT

from mysite.model.base import Base


class Message(Base):
    __tablename__ = "message"
    id = Column(Integer,primary_key=True,autoincrement=True)
    user_id = Column(Integer,doc=u"发留言的用户id")
    message_user_id = Column(Integer,doc=u"接受留言的用户id")
    message = Column(TEXT)
    message_type = Column(Integer,default=0,doc=u"0默认为用户留言，1表示系统留言")
    create_time = Column(Integer,default=lambda: time(), doc=u"留言时间")

    @classmethod
    def get_message_info(cls,connection,message_id):
        return connection.query(Message).filter(Message.id == message_id).scalar()

    @classmethod
    def set_message(cls,connection,user_id,message_user_id,message):
        """对某个人留言"""
        me = Message(user_id=user_id,
                     message_user_id=message_user_id,
                     message=message)
        connection.add(me)
        connection.commit()

    @classmethod
    def get_message_user(cls,connection,message_user_id):
        """获取被人给自己的留言信息"""
        return connection.query(Message).\
            filter(Message.message_user_id == message_user_id)

    @classmethod
    def set_message_to_gov(cls,connection,user_id,message):
        """对官方留言"""
        message = Message(user_id=user_id,message=message,message_type=1)
        connection.add(message)
        connection.commit()

    @classmethod
    def del_message_to_user(cls,connection,message_id):
        """删除留言"""
        connection.query(Message).filter(Message.id==message_id).delete()
        connection.commit()

