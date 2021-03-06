# -*-coding:utf-8-*-
__author__ = ''
from sqlalchemy.schema import Table, Column
from sqlalchemy.types import Integer, Unicode, Float
from sqlalchemy.sql import select
from sqlalchemy import func
from datetime import datetime

from models.base import Base


class Prize(Base):
    u"""优惠码表"""
    __tablename__ = "prize"
    id = Column(Integer, primary_key=True, autoincrement=True)
    coupon = Column(Unicode(255), doc=u"优惠码的信息")
    account = Column(Integer, doc=u"优惠码金额")
    user_id = Column(Integer, doc=u"分配给某些用户")
    share = Column(Integer, doc=u"是否分享，默认为0，没有分享")
    probability = Column(Integer, doc=u"用户概率控制，3表示废弃优惠码")


    @classmethod
    def get_random_prize(cls,connection):
        stmt = connection.query(Prize).\
            filter(Prize.user_id.is_(None)).\
            filter(Prize.probability == 1).\
            order_by(func.rand()).limit(1).scalar()
        if stmt is None:
            stmt = connection.query(Prize).\
                filter(Prize.user_id.is_(None)).\
                order_by(func.rand()).limit(1).scalar()
        return stmt


    @classmethod
    def get_random_prize_not_coupon(cls, connection):
        return connection.query(Prize).\
            filter(Prize.account.in_((20, 35, 50, 90))).limit(1).scalar()

    @classmethod
    def get_user_prize(cls,connection,user_id):
        return connection.query(Prize).filter(Prize.user_id == user_id).scalar()

    @classmethod
    def set_prize_user(cls,connection,prize_id,user_id):
        connection.query(Prize).\
            filter(Prize.id == prize_id).update(
            {
                Prize.user_id: user_id
            }
        )
        connection.commit()

    @classmethod
    def get_share_prize(cls,connection,user_id):
        prize = connection.query(Prize).filter(Prize.user_id == user_id).\
            filter(Prize.share == 0).scalar()
        if prize:
            account = prize.account
            connection.query(Prize).filter(Prize.id == prize.id).update(
                {
                    Prize.user_id: None,
                    Prize.probability: 3
                }
            )
            connection.commit()
            new_prize = connection.query(Prize).\
                filter(Prize.account == account + 10).\
                filter(Prize.user_id.is_(None)).limit(1).scalar()
            connection.query(Prize).filter(Prize.id == new_prize.id).update(
                {
                    Prize.user_id:user_id,
                    Prize.share:1
                }
            )
            connection.commit()
            return True
        return False