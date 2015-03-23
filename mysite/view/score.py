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
    get_TELTS, get_Total, get_GMAT
from mysite.model.stasub import Stasub

@validate_user_login
@allow_cross_domain
def set_user_score():
    if request.method == "POST":
        user_id = session.get("user_id")
        print request.form
        if request.form.get("bginf") is not None:
            bginf = request.form.get("bginf")
            User.update_user_bginf(g.db, user_id, bginf)
        if request.form.get("GRE[sub][0][id]"):
            Stasub.del_sub(g.db,user_id)
            num = 0

            while True:
                if request.form.get("GRE[sub]["+str(num)+"][id]"):
                    sub_id = request.form.get("GRE[sub]["+str(num)+"][id]",0,int)
                    grade = request.form.get("GRE[sub][0][grade]",0,int)
                    sub_type = 0
                    if sub_id >10:
                        sub_type = 1
                    Stasub.set_sub(g.db, sub_id=sub_id, grade=grade,
                                   sub_type=sub_type, user_id=user_id)
                break


        if request.form.get("IELTSmore[R]") is not None:
            LELTSmoreR = request.form.get("IELTSmore[R]", 0, int)
            LELTSmoreL = request.form.get("IELTSmore[L]", 0, int)
            LELTSmoreS = request.form.get("IELTSmore[S]", 0, int)
            LELTSmoreW = request.form.get("IELTSmore[W]", 0, int)
            sub_TELTS = get_TELTS(LELTSmoreS, LELTSmoreL, LELTSmoreR,
                                  LELTSmoreW)
            if request.form.get("GREmore[V]") is not None:
                GREmoreV = request.form.get("GREmore[V]", 0, int)
                GREmoreQ = request.form.get("GREmore[Q]", 0, int)
                GREmoreAW = request.form.get("GREmore[AW]", 0, int)
                sub_GRE = get_gre(GREmoreV, GREmoreQ)
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
            else:
                GMATmoreV = request.form.get("GMATmore[V]", 0, int)
                GMATmoreQ = request.form.get("GMATmore[Q]", 0, int)
                GMATmoreAW = request.form.get("GMATmore[AW]", 0, int)
                GMATmoreIR = request.form.get("GMATmore[IR]", 0, int)
                sub_GMAT = get_GMAT(GMATmoreV, GMATmoreQ)
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
            TOEFLmoreR = request.form.get("TOEFLmore[R]", 0, int)
            TOEFLmoreL = request.form.get("TOEFLmore[L]", 0, int)
            TOEFLmoreS = request.form.get("TOEFLmore[S]", 0, int)
            TOEFLmoreW = request.form.get("TOEFLmore[W]", 0, int)
            sub_TOEFL = get_Total(TOEFLmoreL, TOEFLmoreR, TOEFLmoreS,
                                  TOEFLmoreW)
            if request.form.get("GREmore[V]") is not None:
                GREmoreV = request.form.get("GREmore[V]", 0, int)
                GREmoreQ = request.form.get("GREmore[Q]", 0, int)
                GREmoreAW = request.form.get("GREmore[AW]", 0, int)
                sub_GRE = get_gre(GREmoreV, GREmoreQ)
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
            else:
                GMATmoreV = request.form.get("GMATmore[V]", 0, int)
                GMATmoreQ = request.form.get("GMATmore[Q]", 0, int)
                GMATmoreAW = request.form.get("GMATmore[AW]", 0, int)
                GMATmoreIR = request.form.get("GMATmore[IR]", 0, int)
                sub_GMAT = get_GMAT(GMATmoreV, GMATmoreQ)
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
        return jsonify(status="success")

