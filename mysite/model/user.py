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
    grade = Column(Integer,doc=u"字段，筛选相关")
    type = Column(Integer, doc=u"高中还是大学：1表示大学，0表示高中,3表示研究生")
    description = Column(Unicode(255),doc=u"描述")

    @classmethod
    def get_user_info(cls,connection, user_id):
        return connection.query(User).filter(User.id == user_id)


    @classmethod
    def login_user(cls,connection,email,password):
        return connection.query(User.id).\
            filter(User.email == email).\
            filter(User.password == password).scalar()

    @classmethod
    def register_first(cls,connection,email,password,phone):
        connection.query(User).\
            filter(User.phone==phone).\
            update({User.email:email,User.password:password})

    @classmethod
    def set_user_info_detail(cls,connection, user_id,
                             prevuniversity, prevmajor,
                             type,description):
       connection.query(User).filter(User.id == user_id).\
           update({User.prevuniversity:prevuniversity,
           User.prevmajor:prevmajor,
           User.type:type,
           User.description:description})

    @classmethod
    def set_sms_checknum(cls,connection,phone,checknum):
        user = User(phone=phone,checknum=checknum)
        connection.add(user)
        connection.commit()

    @classmethod
    def get_user_name(cls,connection,user_id):
        return connection.query(User).filter(User.id == user_id).scalar()


    @classmethod
    def get_checknum(cls,connection,phone):
        return connection.query(User.checknum).\
            filter(User.phone == phone).scalar()
