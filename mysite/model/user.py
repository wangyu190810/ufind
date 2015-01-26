# -*-coding:utf-8-*-
__author__ = 'wangyu'
from sqlalchemy import Column, String, TEXT, Integer, Unicode, Float
from base import Base


class User(Base):
    """用户信息表"""
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(80), doc=u"用户名")
    password = Column(String(80), doc=u"密码")
    email = Column(String(80), doc=u"邮箱")
    phone = Column(Integer, doc=u"电话")
    pic = Column(Unicode(255), doc=u"头像")
    GPA = Column(Float(10), doc=u"")
    TOEFL = Column(Float(10), doc=u"")
    GRE = Column(Float(10), doc=u"")
    IELTS = Column(Float(10), doc=u"")
    GMAT = Column(Float(10), doc=u"")
    SAT = Column(Float(10), doc=u"")
    prevuniversity = Column(Unicode(225), doc=u"国内学校")
    prevmajor = Column(Unicode(255), doc=u"专业，如果时高中字段为空")
    gender = Column(Integer, doc=u"性别：1表示男，0表示女")
    type = Column(Integer, doc=u"高中还是大学：1表示大学，0表示高中,3表示研究生")

    @classmethod
    def get_user_info(cls,connection, user_id):
        return connection.query(User).filter(User.id == user_id)







