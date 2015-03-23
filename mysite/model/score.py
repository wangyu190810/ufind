# -*-coding:utf-8-*-
__author__ = 'wangyu'
from sqlalchemy import Column, String, TEXT, Integer, Unicode, Float
from base import Base


class Score(Base):
    """用户信息表"""
    __tablename__ = "score"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, default=0, doc=u"用户id")
    rank = Column(Integer, default=0, doc=u"")
    TOEFL_r = Column(Integer, default=0, doc=u"")
    TOEFL_l = Column(Integer, default=0, doc=u"")
    TOEFL_s = Column(Integer, default=0, doc=u"")
    TOEFL_w = Column(Integer, default=0, doc=u"")
    IELTS_r = Column(Integer, default=0, doc=u"")
    IELTS_l = Column(Integer, default=0, doc=u"")
    IELTS_s = Column(Integer, default=0, doc=u"")
    IELTS_w = Column(Integer, default=0, doc=u"")
    GRE_v = Column(Integer, default=0, doc=u"")
    GRE_q = Column(Integer, default=0, doc=u"")
    GRE_aw = Column(Integer, default=0, doc=u"")
    GMAT_v = Column(Integer, default=0, doc=u"")
    GMAT_q = Column(Integer, default=0, doc=u"")
    GMAT_aw = Column(Integer, default=0, doc=u"")
    GMAT_ir = Column(Integer, default=0, doc=u"")
    SAT_cr = Column(Integer, default=0, doc=u"")
    SAT_m = Column(Integer, default=0, doc=u"")
    SAT_w = Column(Integer, default=0, doc=u"")

    @classmethod
    def set_user_info(cls,
                      connection,
                      user_id,
                      rank=None,
                      TOEFL_r=None,
                      TOEFL_l=None,

                      TOEFL_s=None,
                      TOEFL_w=None,
                      IELTS_r=None,
                      IELTS_l=None,
                      IELTS_s=None,
                      IELTS_w=None,
                      GRE_v=None,
                      GRE_q=None,
                      GRE_aw=None,
                      GMAT_v=None,
                      GMAT_q=None,
                      GMAT_aw=None,
                      GMAT_ir=None,
                      SAT_cr=None,
                      SAT_m=None,
                      SAT_w=None):
            cls.del_user_score(connection=connection,user_id=user_id)
            score = Score(user_id=user_id,rank=rank, TOEFL_r=TOEFL_r, TOEFL_l=TOEFL_l,
                          TOEFL_s=TOEFL_s, TOEFL_w=TOEFL_w, IELTS_r=IELTS_r,
                          IELTS_l=IELTS_l,
                          IELTS_s=IELTS_s,
                          IELTS_w=IELTS_w,
                          GRE_v=GRE_v,
                          GRE_q=GRE_q,
                          GRE_aw=GRE_aw,
                          GMAT_v=GMAT_v,
                          GMAT_q=GMAT_q,
                          GMAT_aw=GMAT_aw,
                          GMAT_ir=GMAT_ir,
                          SAT_cr=SAT_cr,
                          SAT_m=SAT_m,
                          SAT_w=SAT_w
            )
            connection.add(score)
            connection.commit()

    @classmethod
    def del_user_score(cls,connection,user_id):
        u"""用户的分数只能有一个，所以采用只要从新填写分数，自动删除之前的分数"""
        connection.query(Score).filter(Score.user_id == user_id).delete()
        connection.commit()

    @classmethod
    def get_user_score(cls,connection,user_id):
        u"""获取用户的成绩"""
        return connection.query(Score).filter(Score.user_id == user_id).scalar()