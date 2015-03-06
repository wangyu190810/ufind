# -*-coding:utf-8-*-
__author__ = 'wangyu'
from sqlalchemy import Column, String, Integer, Unicode, Float,func

import time

from base import Base


class User(Base):

    """用户信息表"""

    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(80), doc=u"用户名")
    password = Column(String(80), doc=u"密码")
    email = Column(String(80), doc=u"邮箱")
    phone = Column(Integer, doc=u"电话")
    checknum = Column(Integer, doc=u"验证码")
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
    grade = Column(Integer, doc=u"字段，筛选相关")
    type = Column(Integer, doc=u"高中还是大学：0表示大学，1表示高中,3表示研究生")
    description = Column(Unicode(255), doc=u"描述")
    bginf = Column(Unicode(255), doc=u"背景信息")

    @classmethod
    def get_user_info(cls, connection, user_id):
        return connection.query(User).filter(User.id == user_id).scalar()

    @classmethod
    def login_user(cls, connection, email=None, phone=None, password=None,):
        if phone is None:
            return connection.query(User). \
                filter(User.email == email). \
                filter(User.password == password).scalar()
        elif email is None:
            return connection.query(User).\
                filter(User.phone == phone).\
                filter(User.password == password).scalar()

    @classmethod
    def register_first(cls, connection, email, password, phone):
        connection.query(User). \
            filter(User.phone == phone). \
            update({User.email: email, User.password: password})
        connection.commit()

    @classmethod
    def register_second(cls, connection, phone, username,
                        university_id, major_id, gpa,user_type):
        connection.query(User).filter(User.phone == phone).update(
            {User.username: username,
             User.prevuniversity: university_id,
             User.prevmajor: major_id,
             User.GPA: gpa,
             User.type: user_type}
        )
        connection.commit()

    @classmethod
    def set_user_info_detail(cls, connection,
                             user_id, prevuniversity,
                             prevmajor, type,
                             description):
        connection.query(User).filter(User.id == user_id).update(
            {User.prevuniversity: prevuniversity,
             User.prevmajor: prevmajor,
             User.type: type,
             User.description: description})
        connection.commit()

    @classmethod
    def set_sms_checknum(cls, connection, phone, checknum):
        phonenum = connection.query(User.phone). \
            filter(User.phone == phone).scalar()
        if len(str(phonenum)) < 10:
            user = User(phone=phone, checknum=checknum)
            connection.add(user)
            connection.commit()
        else:
            connection.query(User).filter(User.phone == phone).update(
                {User.checknum: checknum}
            )
            connection.commit()

    @classmethod
    def get_user_name(cls, connection, user_id):
        return connection.query(User).filter(User.id == user_id).scalar()

    @classmethod
    def get_checknum(cls, connection, phone):
        return connection.query(User.checknum). \
            filter(User.phone == phone).scalar()

    @classmethod
    def change_password(cls, connection, phone, password):
        connection.query(User).filter(User.phone == phone).update({
            User.password: password})
        connection.commit()

    @classmethod
    def get_user_info_by_phone(cls, connection, phone):
        return connection.query(User).filter(User.phone == phone).scalar()


class UserFollow(Base):

    __tablename__ = "user_follow"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, doc=u"用户id")
    follow_user_id = Column(Integer, doc=u"关注者的id")
    create_time = Column(Integer, default=lambda: time.time(), doc=u"关注时间")

    @classmethod
    def set_follow(cls, connection, user_id, follow_user_id):
        """关注用户"""
        user_follow = UserFollow(user_id=user_id, follow_user_id=follow_user_id)
        connection.add(user_follow)
        connection.commit()

    @classmethod
    def del_follow_id(cls, connection, user_id, follow_user_id):
        """取消关注"""
        connection.query(UserFollow).\
            filter(UserFollow.user_id == user_id).\
            filter(UserFollow.follow_user_id == follow_user_id).delete()
        connection.commit()

    @classmethod
    def get_follow_id(cls, connection, user_id):
        """关注列表"""
        return connection.query(UserFollow).\
            filter(UserFollow.user_id == user_id)

    @classmethod
    def get_follow_to_user(cls,connection,user_id,follow_user_id):
        """或者两个用户之间的关注关系"""
        return connection.query(UserFollow).\
            filter(UserFollow.user_id == user_id).\
            filter(UserFollow.follow_user_id == follow_user_id).scalar()

    @classmethod
    def get_follow_count_user(cls,connection,follow_user_id):
        """获取粉丝数量"""
        return connection.query(func.count(UserFollow)).\
            filter(UserFollow.follow_user_id == follow_user_id).scalar()
