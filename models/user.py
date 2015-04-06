# coding: utf-8
# email: khahux@163.com

import time

from sqlalchemy import Column, String, Integer, Unicode, Float, func

from models.base import Base


class User(Base):

    u"""用户信息表"""

    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(80), doc=u"用户名")
    password = Column(String(80), doc=u"密码")
    email = Column(String(80), doc=u"邮箱")
    phone = Column(Integer, doc=u"电话")
    checknum = Column(Integer, doc=u"验证码")
    checknum_time = Column(Integer, doc=u"验证码时间")
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
    grade = Column(Unicode(255), doc=u"申请的级别学生的级别")
    type = Column(Integer,
                  doc=u"高中还是大学：0表示高中，1表示大学,3表示研究生")
    description = Column(Unicode(255), doc=u"描述")
    bginf = Column(Unicode(255), doc=u"背景信息")
    create_time = Column(Integer, doc=u"注册时间")

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
                        university_id, major_id, gpa, user_type,
                        create_time):
        connection.query(User).filter(User.phone == phone).update(
            {User.username: username,
             User.prevuniversity: university_id,
             User.prevmajor: major_id,
             User.GPA: gpa,
             User.type: user_type,
             User.create_time: create_time}
        )
        connection.commit()

    @classmethod
    def set_user_info_detail(cls, connection, user_id, prevuniversity, prevmajor, type, description):
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
            user = User(phone=phone, checknum=checknum, checknum_time=time.time())
            connection.add(user)
            connection.commit()
        else:
            connection.query(User).filter(User.phone == phone).update({
                User.checknum: checknum,
                User.checknum_time: time.time()
            })
            connection.commit()

    @classmethod
    def get_user_name(cls, connection, user_id):
        u"""用户的信息通过id获取"""
        return connection.query(User).filter(User.id == user_id).scalar()

    @classmethod
    def get_checknum(cls, connection, phone):
        u"""验证码检测"""
        return connection.query(User). \
            filter(User.phone == phone).scalar()

    @classmethod
    def change_password(cls, connection, phone, password):
        u"""手机修改密码"""
        connection.query(User).filter(User.phone == phone).update({
            User.password: password})
        connection.commit()

    @classmethod
    def change_password_old(cls, connection, user_id, password, passwordold):
        u"""更新用户密码"""
        if not connection.query(User).\
                filter(User.id == user_id).\
                filter(User.password == passwordold).scalar():
            return False

        connection.query(User).\
            filter(User.id == user_id).\
            filter(User.password == passwordold).update({User.password: password})
        return True

    @classmethod
    def update_user_phone(cls, connection, user_id, phone, checknum):
        u"""更新个人电话"""
        connection.query(User).filter(user_id).update({
            User.phone: phone,
            User.checknum: checknum,
            User.checknum_time: time.time()
        })
        connection.commit()

    @classmethod
    def get_user_info_by_phone(cls, connection, phone):
        u"""电话获取用户分数"""
        return connection.query(User).filter(User.phone == phone).scalar()

    @classmethod
    def update_user_bginf(cls, connection, user_id, bginf):
        u"""更新个人背景信息"""
        connection.query(User).filter(User.id == user_id).\
            update({User.bginf: bginf})
        connection.commit()

    @classmethod
    def update_user_grade(cls, connection, user_id, grade):
        u"""更新个人学历"""
        connection.query(User).filter(User.id == user_id).\
            update({User.grade: grade})
        connection.commit()

    @classmethod
    def update_user_info(cls, connection,
                         user_id, username,
                         phone, email,
                         prevuniversity, prevmajor):
        u"""用户资料更新"""
        connection.query(User).filter(User.id == user_id).update(
            {User.username: username,
             User.phone: phone,
             User.email: email,
             User.prevuniversity: prevuniversity,
             User.prevmajor: prevmajor}
        )
        connection.commit()

    @classmethod
    def update_user_pic(cls, connection, user_id, pic):
        u"""更新用户的头像"""
        connection.query(User).filter(User.id == user_id).update(
            {User.pic: pic}
        )
        connection.commit()

    @classmethod
    def update_user_description(cls, connection, user_id, description):
        u"""更新用户描述"""
        connection.query(User).filter(User.id == user_id).update(
            {
                User.description: description
            }
        )
        connection.commit()

    @classmethod
    def update_user_score(cls, connection, user_id, gre=None, toefl=None, lelts=None, GMAT=None, sat=None):
        u"""分数计算结果的更新"""
        connection.query(User).filter(User.id == user_id).update({
            User.GRE: gre,
            User.GMAT: GMAT,
            User.TOEFL: toefl,
            User.IELTS: lelts,
            User.SAT: sat
        })
        connection.commit()


class UserFollow(Base):
    __tablename__ = "user_follow"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, doc=u"用户id")
    follow_user_id = Column(Integer, doc=u"关注者的id")
    create_time = Column(Integer, default=lambda: time.time(), doc=u"关注时间")

    @classmethod
    def set_follow(cls, connection, user_id, follow_user_id):
        u"""关注用户"""
        user_follow = UserFollow(user_id=user_id, follow_user_id=follow_user_id)
        connection.add(user_follow)
        connection.commit()

    @classmethod
    def del_follow_id(cls, connection, user_id, follow_user_id):
        u"""取消关注"""
        connection.query(UserFollow).\
            filter(UserFollow.user_id == user_id).\
            filter(UserFollow.follow_user_id == follow_user_id).delete()
        connection.commit()

    @classmethod
    def get_follow_id(cls, connection, user_id):
        u"""我的关注列表"""
        return connection.query(UserFollow).\
            filter(UserFollow.user_id == user_id)

    @classmethod
    def get_follow_user_id(cls, connection, follow_user_id):
        u"""别人关注我的列表"""
        return connection.query(UserFollow).filter(
            UserFollow.follow_user_id == follow_user_id
        )

    @classmethod
    def get_follow_to_user(cls, connection, user_id, follow_user_id):
        u"""或者两个用户之间的关注关系"""
        return connection.query(UserFollow).\
            filter(UserFollow.user_id == user_id).\
            filter(UserFollow.follow_user_id == follow_user_id).scalar()

    @classmethod
    def get_follow_count_user(cls, connection, follow_user_id):
        u"""获取粉丝数量"""
        return connection.query(func.count(UserFollow)).\
            filter(UserFollow.follow_user_id == follow_user_id).scalar()
