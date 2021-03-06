# coding: utf-8
# email: khahux@163.com

from time import time

from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, Unicode
from sqlalchemy.sql import func,text

from models.base import Base


class Offer(Base):
    __tablename__ = "offer"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer, doc=u"用户id", index=True)
    university_id = Column(Integer, index=True,doc=u"学校的id")
    major_id = Column(Integer, doc=u"专业id")
    result = Column(Integer, doc=u"状态位")
    grade = Column(Unicode(80), doc=u"master硕士，pa博士")
    offer_type = Column(Unicode(80), doc=u"offer的类型，没有没有奖学金")
    scholarship = Column(Integer, doc=u"奖学金的数值")
    scholarship_type = Column(Unicode(80), doc=u"奖学金的类型")
    school1_id = Column(Integer, doc=u"学院ID")
    school2_id = Column(Integer, doc=u"学院ID")
    school3_id = Column(Integer, doc=u"学院ID")
    create_time = Column(Integer, default=lambda: time())
    user_type = Column(Integer,doc=u"用户类型")
    wechat = Column(Unicode(255),doc=u"每个offer拥有唯一的微信图片")
    offer_status = Column(Integer,doc=u"offer是否可用来做统计,默认1可以统计,2不可统计")


    @classmethod
    def set_offer(cls, connection, user_id,
                  university_id, major_id,
                  result, grade,
                  school1_id,
                  school2_id,
                  school3_id,
                  offer_type,
                  user_type,
                  wechat,
                  offer_status,
                  scholarship=None,
                  scholarship_type=None,

                  ):
        offer = Offer(user_id=user_id, university_id=university_id,
                      major_id=major_id, result=result,
                      grade=grade,
                      school1_id=school1_id,
                      school2_id=school2_id,
                      school3_id=school3_id,
                      user_type=user_type,
                      offer_type=offer_type,
                      scholarship=scholarship,
                      scholarship_type=scholarship_type,
                      wechat=wechat,
                      offer_status=offer_status)
        connection.add(offer)
        connection.commit()

    @classmethod
    def set_offer_mobile(cls, connection, user_id,
                            university_id, major_id,
                            school1_id, user_type,
                            wechat,grade,
                            school2_id,school3_id,
                            offer_type,offer_status):
        print major_id
        offer = Offer(user_id=user_id,
                      university_id=university_id,
                      major_id=major_id,
                      school1_id=school1_id,
                      school2_id=school2_id,
                      school3_id=school3_id,
                      user_type=user_type,
                      offer_type=offer_type,
                      grade=grade,
                      wechat=wechat,
                      offer_status=offer_status
              )
        connection.add(offer)
        connection.commit()

    @classmethod
    def get_mobile_user_last_offer(cls,connection,user_id):
        return connection.query(func.max(Offer.create_time),
                                Offer.university_id,
                                Offer.wechat).filter(Offer.user_id == user_id)


    @classmethod
    def get_offer_student(cls, connection, unviersity_id, major_id, user_type):
        """根据学校和专业随机的返回两个学生的id"""
        return connection.query(Offer). \
            filter(Offer.university_id == unviersity_id). \
            filter(Offer.major_id == major_id).\
            filter(Offer.user_type == user_type).limit(6)

    @classmethod
    def get_offer_student_info(cls, connection, student_id):
        u"""根据学生的id查看学生的offer"""
        return connection.query(Offer). \
            filter(Offer.user_id == student_id)

    @classmethod
    def get_offer_num(cls, connection, university_id,user_type=None):
        """查看当前学校的off数量"""
        if user_type is None:
            return connection.query(func.count(Offer)). \
                filter(Offer.university_id == university_id).\
                filter(Offer.offer_status == 1).\
                filter(Offer.result == 1).scalar()

        return connection.query(func.count(Offer)). \
            filter(Offer.university_id == university_id).\
            filter(Offer.user_type == user_type).\
            filter(Offer.offer_status == 1).\
            filter(Offer.result == 1).scalar()


    @classmethod
    def get_user_id_from_university(cls, connection, university_id,

                                    major_id=None,user_type=None,grade=None):
        """根据学校找学生iD"""
        if major_id is None and user_type is None and grade is None:

            return connection.query(Offer). \
                filter(Offer.university_id == university_id).\
                filter(Offer.offer_status == 1)
        elif user_type is not None and major_id is None:
            return connection.query(Offer).filter(
                Offer.university_id == university_id). \
                filter(Offer.user_type == user_type).\
                filter(Offer.offer_status == 1)
        elif user_type is not None and major_id is not None and grade is not None:
             return connection.query(Offer).filter(
            Offer.university_id == university_id). \
            filter(Offer.major_id == major_id).\
            filter(Offer.user_type == user_type).\
                 filter(Offer.grade == grade)
        elif major_id is None and grade is None and user_type is not None:
            return connection.query(Offer).filter(
                Offer.university_id == university_id).filter(
                Offer.user_type == user_type
            ).filter(Offer.offer_status==1)

        return connection.query(Offer).filter(
            Offer.university_id == university_id). \
            filter(Offer.major_id == major_id).\
            filter(Offer.user_type == user_type).\
            filter(Offer.offer_status == 1)

    @classmethod
    def get_user_id_from_major(cls, connection, major_id,user_type=None):
        """根据专业id查找学生信息"""
        if user_type is not None:
            return connection.query(Offer).\
                filter(Offer.major_id == major_id).\
                filter(Offer.user_type == user_type).limit(6)

        return connection.query(Offer).\
            filter(Offer.major_id == major_id).limit(6)

    @classmethod
    def update_offer_status(cls,connection,user_id):
        u"""用户在移动端注册，完成他的offer可见性"""
        connection.query(Offer).filter(Offer.user_id == user_id).update(
            {
                Offer.offer_status:1
            }
        )
        connection.commit()

    @classmethod
    def get_site_offer_num(cls,connection,user_type=None):
        """全站offer数量"""
        if user_type is None:
            return connection.query(func.count(Offer.id)).scalar()
        return connection.query(func.count(Offer.id)).\
            filter(Offer.user_type == user_type).\
            filter(Offer.offer_status == 1).scalar()


    @classmethod
    def get_offer_num_from_major(cls, connection, university_id, major_id):
        return connection.query(func.count(Offer.id)).\
            filter(Offer.university_id == university_id).\
            filter(Offer.major_id == major_id).\
            filter(Offer.offer_status == 1).\
            filter(Offer.result == 1).scalar()

    @classmethod
    def del_same_offer(cls, connection, university_id, major_id, user_id):
        u"""删除用户的重复offer"""
        connection.query(Offer).\
            filter(Offer.university_id == university_id).\
            filter(Offer.user_id == user_id).\
            filter(Offer.major_id == major_id).delete()
        connection.commit()

    @classmethod
    def set_user_offer_result(cls,connection,user_id):
        u"""用户offer可以被统计"""
        connection.query(Offer).\
            filter(Offer.user_id == user_id).\
            filter(Offer.result != 1).update(
            {
                Offer.result: 1,
                Offer.offer_status: 1
            }
        )
        connection.commit()

    @classmethod
    def get_index_from_offer_num(cls, connection,university_id,school_id,user_type):

        sql = text("""(select count(user_id) as countmajor,major_id as id from offer
        where university_id=:university_id_1 and  school1_id=:school_id_1
        group by major_id order by countmajor desc) union
        (select 0 as countmajor, id from major
        where university_id=:university_id_2 and  faculty_id=:school_id_2 and id not
        in (select major_id from offer where university_id=:university_id_3 and
        school1_id=:school_id_3) order by rand() limit 3)""")

        if user_type is None:

            sql = """(select count(user_id) as countmajor,major_id as id
        from offer where university_id=%s and  school1_id=%s  group by
        major_id order by countmajor desc) union (select 0 as countmajor,
        id from major where university_id=%s and  faculty_id=%s
        and id not in (select major_id from offer where university_id=%s and
        school1_id=%s )
        order by rand() limit 8)""" %(university_id,school_id,
                                      university_id,school_id,
                                      university_id,school_id)
            return connection.execute(sql)
        sql = """(select count(user_id) as countmajor,major_id as id
        from offer where university_id=%s and  school1_id=%s and user_type =%s group by
        major_id order by countmajor desc) union (select 0 as countmajor,
        id from major where university_id=%s and  faculty_id=%s and major_type = %s
        and id not in (select major_id from offer where university_id=%s and
        school1_id=%s and user_type=%s)
        order by rand() limit 8)""" %(university_id,school_id,user_type,
                                      university_id,school_id,user_type,
                                      university_id,school_id,user_type)


        return connection.execute(sql)
