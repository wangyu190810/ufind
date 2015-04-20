# -*-coding:utf-8-*-
__author__ = ''
from sqlalchemy.schema import Table, Column
from sqlalchemy.types import Integer, Unicode, Float
from sqlalchemy.sql import select
from sqlalchemy import func
from datetime import datetime

from mysite.model.base import metadata, Base


class Prize(Base):
    u"""优惠码表"""
    id = Column(Integer,primary_key=True,autoincrement=True)
    coupon = Column(Unicode(255),doc=u"优惠码的信息")
    account = Column(Integer,doc=u"优惠码金额")
    user_id = Column(Integer,doc=u"分配给某些用户")

    @classmethod
    def get_random_prize(cls,connection):
        return connection.query(func.random(Prize)).filter(Prize.user_id is None).scalar()

    @classmethod
    def set_prize_user(cls,connection,prize_id,user_id):
        connection.query(Prize).\
            filter(Prize.id == prize_id).update(
            {
                Prize.user_id:user_id
            }
        )
