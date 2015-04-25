#! /usr/bin/python
# -*- coding:utf-8 -*-
# Filename: university.py
#Author: wangyu190810
#E-mail: wo190810401@gmail.com
#Date: 2015-01-22
#Description:

import json
from flask import request, jsonify, g, session
from mysite.model.university import University
from mysite.model.faculty import Faculty
from mysite.model.major import Major
from mysite.model.user import User
from mysite.model.score import Score
from mysite.view.base import allow_cross_domain, validate_user_login, get_gre, \
    get_TELTS, get_Total, get_GMAT,get_SAT
from mysite.model.stasub import Stasub

@validate_user_login
@allow_cross_domain
def set_user_score():
    if request.method == "POST":
        user_id = session.get("user_id")
        if request.form.get("bginf") is not None:
            bginf = request.form.get("bginf")
            User.update_user_bginf(g.db, user_id, bginf)
        print request.form
        Stasub.del_sub(g.db,user_id)
        if request.form.get("GREmore[sub][0][id]"):
            num = 0

            while True:
                if request.form.get("GREmore[sub]["+str(num)+"][id]"):
                    sub_id = request.form.get("GREmore[sub]["+str(num)+"][id]",0,int)
                    grade = request.form.get("GREmore[sub]["+str(num)+"][grade]",0,int)
                    sub_type = 0
                    if sub_id >10:
                        sub_type = 1
                    Stasub.set_sub(g.db, sub_id=sub_id, grade=grade,
                                   sub_type=sub_type, user_id=user_id)
                    num += 1
                else:
                    break

        #Stasub.del_sub(g.db,user_id)
        if request.form.get("SATmore[sub][0][grade]"):
            num = 0

            while True:
                if request.form.get("SATmore[sub]["+str(num)+"][id]"):
                    sub_id = request.form.get("SATmore[sub]["+str(num)+"][id]",0,int)
                    grade = request.form.get("SATmore[sub]["+str(num)+"][grade]",0,int)
                    sub_type = 0
                    if sub_id >10:
                        sub_type = 1
                    Stasub.set_sub(g.db, sub_id=sub_id, grade=grade,
                                   sub_type=sub_type, user_id=user_id)
                    num += 1
                else:
                    break

        if request.form.get("IELTSmore[R]") is not None:
            LELTSmoreR = request.form.get("IELTSmore[R]", float)
            LELTSmoreL = request.form.get("IELTSmore[L]", float)
            LELTSmoreS = request.form.get("IELTSmore[S]", float)
            LELTSmoreW = request.form.get("IELTSmore[W]", float)
            sub_TELTS = request.form.get("IELTSmore[total]", float)
            #sub_TELTS = get_TELTS(LELTSmoreS, LELTSmoreL, LELTSmoreR,
            #                      LELTSmoreW)
            if request.form.get("GREmore[V]") is not None:
                GREmoreV = request.form.get("GREmore[V]", int)
                GREmoreQ = request.form.get("GREmore[Q]", int)
                GREmoreAW = request.form.get("GREmore[AW]", float)
                sub_GRE = request.form.get("GREmore[total]", int)

                User.update_user_score(g.db, user_id, gre=sub_GRE,
                                       lelts=sub_TELTS)
                Score.set_user_info(connection=g.db, user_id=user_id,
                                    IELTS_r=LELTSmoreR,
                                    IELTS_l=LELTSmoreL,
                                    IELTS_s=LELTSmoreS,
                                    IELTS_w=LELTSmoreW,
                                    GRE_v=GREmoreV,
                                    GRE_q=GREmoreQ,
                                    GRE_aw=GREmoreAW
                )
            elif request.form.get("SATmore[M]") is not None:
                sat_m = request.form.get("SATmore[M]",  int)
                sat_cr = request.form.get("SATmore[CR]", int)
                sat_w = request.form.get("SATmore[W]", int)
                sub_sat= request.form.get("SATmore[total]", int)
                #sub_sat = get_SAT(sat_cr,sat_w,sat_m)
                User.update_user_score(g.db,user_id=user_id,
                                       lelts=sub_TELTS,
                                       sat=sub_sat)
                Score.set_user_info(connection=g.db,
                                    user_id=user_id,
                                    IELTS_r=LELTSmoreR,
                                    IELTS_l=LELTSmoreL,
                                    IELTS_s=LELTSmoreS,
                                    IELTS_w=LELTSmoreW,
                                    SAT_m=sat_m,
                                    SAT_w=sat_w,
                                    SAT_cr=sat_cr
                )
            elif request.form.get("GMATmore[V]") is not None:
                GMATmoreV = request.form.get("GMATmore[V]", int)
                GMATmoreQ = request.form.get("GMATmore[Q]", int)
                GMATmoreAW = request.form.get("GMATmore[AW]", float)
                GMATmoreIR = request.form.get("GMATmore[IR]", int)
                sub_GMAT = request.form.get("GMATmore[total]", int)
                User.update_user_score(g.db, user_id=user_id,
                                       lelts=sub_TELTS, GMAT=sub_GMAT)
                Score.set_user_info(connection=g.db,
                                    user_id=user_id,
                                    IELTS_r=LELTSmoreR,
                                    IELTS_l=LELTSmoreL,
                                    IELTS_s=LELTSmoreS,
                                    IELTS_w=LELTSmoreW,
                                    GMAT_v=GMATmoreV,
                                    GMAT_q=GMATmoreQ,
                                    GMAT_aw=GMATmoreAW,
                                    GMAT_ir=GMATmoreIR

                )
        elif request.form.get("TOEFLmore[R]") is not None:
            TOEFLmoreR = request.form.get("TOEFLmore[R]", int)
            TOEFLmoreL = request.form.get("TOEFLmore[L]", int)
            TOEFLmoreS = request.form.get("TOEFLmore[S]",  int)
            TOEFLmoreW = request.form.get("TOEFLmore[W]", int)
            sub_TOEFL = request.form.get("TOEFLmore[total]",  int)
            #sub_TOEFL = get_Total(TOEFLmoreL, TOEFLmoreR, TOEFLmoreS,
            #                      TOEFLmoreW)
            if request.form.get("GREmore[V]") is not None:
                GREmoreV = request.form.get("GREmore[V]",  int)
                GREmoreQ = request.form.get("GREmore[Q]",  int)
                GREmoreAW = request.form.get("GREmore[AW]",  float)
                sub_GRE = request.form.get("GREmore[total]",  int)
                #sub_GRE = get_gre(GREmoreV, GREmoreQ)
                User.update_user_score(g.db, user_id=user_id, gre=sub_GRE,
                                       toefl=sub_TOEFL)
                Score.set_user_info(connection=g.db, user_id=user_id,
                                    TOEFL_r=TOEFLmoreR,
                                    TOEFL_l=TOEFLmoreL,
                                    TOEFL_s=TOEFLmoreS,
                                    TOEFL_w=TOEFLmoreW,
                                    GRE_v=GREmoreV,
                                    GRE_q=GREmoreQ,
                                    GRE_aw=GREmoreAW

                )
            elif request.form.get("SATmore[M]") is not None:
                sat_m = request.form.get("SATmore[M]",  int)
                sat_cr = request.form.get("SATmore[CR]",  int)
                sat_w = request.form.get("SATmore[W]",  int)
                sub_sat= request.form.get("SATmore[total]",  int)
                User.update_user_score(g.db,user_id=user_id,
                                       toefl=sub_TOEFL,
                                       sat=sub_sat)
                Score.set_user_info(connection=g.db,
                                    user_id=user_id,
                                    TOEFL_r=TOEFLmoreR,
                                    TOEFL_l=TOEFLmoreL,
                                    TOEFL_s=TOEFLmoreS,
                                    TOEFL_w=TOEFLmoreW,
                                    SAT_m=sat_m,
                                    SAT_w=sat_w,
                                    SAT_cr=sat_cr
                )
            else:
                GMATmoreV = request.form.get("GMATmore[V]", int)
                GMATmoreQ = request.form.get("GMATmore[Q]", int)
                GMATmoreAW = request.form.get("GMATmore[AW]", float)
                GMATmoreIR = request.form.get("GMATmore[IR]",  int)
                sub_GMAT = request.form.get("GMATmore[total]", int)
                User.update_user_score(g.db, user_id=user_id,
                                       toefl=sub_TOEFL, GMAT=sub_GMAT)
                Score.set_user_info(connection=g.db, user_id=user_id,
                                    TOEFL_r=TOEFLmoreR,
                                    TOEFL_l=TOEFLmoreL,
                                    TOEFL_s=TOEFLmoreS,
                                    TOEFL_w=TOEFLmoreW,
                                    GMAT_v=GMATmoreV,
                                    GMAT_q=GMATmoreQ,
                                    GMAT_aw=GMATmoreAW,
                                    GMAT_ir=GMATmoreIR
                )
        User.set_user_active(g.db,user_id)
        return jsonify(status="success")

