#! /usr/bin/python
#-*- coding:utf-8 -*-
#Filename: message.py
#Author: wangyu190810
#E-mail: wo190810401@gmail.com
#Date: 2014-12-29
#Description: 

from sqlalchemy import Column,Integer,String,TEXT,Date,DateTime

from time import time
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
    def set_message(cls,connection,user_id,message_user_id,message):
        me = Message(user_id=user_id,
                     message_user_id=message_user_id,
                     message=message)
        connection.add(me)
        connection.commit()

    @classmethod
    def get_message(cls,connection,user_id):
        return connection.query(Message).\
            filter(Message.user_id == user_id)

    @classmethod
    def set_message_to_gov(cls,connection,user_id,message):
        message = Message(user_id=user_id,message=message,message_type=1)
        connection.add(message)
        connection.commit()
