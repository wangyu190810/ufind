#! /usr/bin/python
# -*- coding:utf-8 -*-
#Filename: university.py
#Author: wangyu190810
#E-mail: wo190810401@gmail.com
#Date: 2015-01-22
#Description:

import json
from flask import request, jsonify, g ,session
from mysite.model.university import University
from mysite.model.faculty import Faculty
from mysite.model.major import Major
from mysite.model.user import User
from mysite.model.score import Score
from mysite.view.base import allow_cross_domain,validate_user_login


@validate_user_login
@allow_cross_domain
def set_user_score():
    print request.data
    if request.method == "POST":
        user_id = session.get("user_id")
        print request.form
        if request.form.get("bginf") is not None:
            bginf = request.form.get("bginf")
            User.update_user_bginf(g.db,user_id,bginf)
        if request.form.get("IELTSmore[R]") is not None:
            LELTSmoreR = request.form.get("IELTSmore[R]",0,int)
            LELTSmoreL = request.form.get("IELTSmore[L]")
            LELTSmoreS = request.form.get("IELTSmore[S]")
            LELTSmoreW = request.form.get("IELTSmore[W]")

            if request.form.get("GERmore[V]") is not None:
                GREmoreV = request.form.get("GERmore[V]")
                GREmoreQ = request.form.get("GERmore[Q]")
                GREmoreAW = request.form.get("GERmore[AW]")
                print GREmoreAW,"GREmoreAW"
                Score.set_user_info(connection=g.db,user_id=user_id,
                                    IELTS_r=LELTSmoreR,
                                    IELTS_l=LELTSmoreL,
                                    IELTS_s=LELTSmoreS,
                                    IELTS_w=LELTSmoreW,
                                    GRE_v=GREmoreV,
                                    GRE_q=GREmoreQ,
                                    GRE_aw=GREmoreAW

                                    )
            else:
                GMATmoreV = request.form.get("GMATmore[V]")
                GMATmoreQ = request.form.get("GMATmore[Q]")
                GMATmoreAW = request.form.get("GMATmore[AW]")
                GMATmoreIR = request.form.get("GMATmore[IR]")
                print GMATmoreAW,"GMATmoreAW"
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
            TOEFLmoreR = request.form.get("TOEFLmore[R]")
            TOEFLmoreL = request.form.get("TOEFLmore[L]")
            TOEFLmoreS = request.form.get("TOEFLmore[S]")
            TOEFLmoreW = request.form.get("TOEFLmore[W]")

            if request.form.get("GERmore[V]") is not None:
                GREmoreV = request.form.get("GERmore[V]")
                GREmoreQ = request.form.get("GERmore[Q]")
                GREmoreAW = request.form.get("GERmore[AW]")
                print GREmoreAW,"GREmoreAV"
                Score.set_user_info(connection=g.db,user_id=user_id,
                                    TOEFL_r =TOEFLmoreR,
                                    TOEFL_l =TOEFLmoreL,
                                    TOEFL_s =TOEFLmoreS,
                                    TOEFL_w =TOEFLmoreW,
                                    GRE_v=GREmoreV,
                                    GRE_q=GREmoreQ,
                                    GRE_aw=GREmoreAW

                                    )
            else:
                GMATmoreV = request.form.get("GMATmore[V]")
                GMATmoreQ = request.form.get("GMATmore[Q]")
                GMATmoreAW = request.form.get("GMATmore[AW]")
                GMATmoreIR = request.form.get("GMATmore[IR]")
                print GMATmoreIR,"GMATmoreIR"
                Score.set_user_info(connection=g.db,user_id=user_id,
                                    TOEFL_r =TOEFLmoreR,
                                    TOEFL_l =TOEFLmoreL,
                                    TOEFL_s =TOEFLmoreS,
                                    TOEFL_w =TOEFLmoreW,
                                    GMAT_v=GMATmoreV,
                                    GMAT_q=GMATmoreQ,
                                    GMAT_aw=GMATmoreAW,
                                    GMAT_ir=GMATmoreIR
                                    )
        return jsonify(status="success")

