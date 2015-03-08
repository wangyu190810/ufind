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
        data = request.data
        print request.form
        user_id = session.get("user_id")
        if request.form.get("IELTSmore[R]") is not None:
            LELTSmoreR = request.form.get("IELTSmore[R]",0,int)
            LELTSmoreL = request.form.get("IELTSmore[L]")
            LELTSmoreS = request.form.get("IELTSmore[S]")
            LELTSmoreW = request.form.get("IELTSmore[W]")

            if request.form.get("GERmore[R]") is not None:
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
                GMATmoreV = request.form.get("GMATmoreV")
                GMATmoreQ = request.form.get("GMATmoreQ")
                GMATmoreAW = request.form.get("GMATmoreAW")
                GMATmoreIR = request.form.get("GMATmoreIR")
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

            if request.form.get("GERmore[R]") is not None:
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
                GMATmoreV = request.form.get("GMATmoreV")
                GMATmoreQ = request.form.get("GMATmoreQ")
                GMATmoreAW = request.form.get("GMATmoreAW")
                GMATmoreIR = request.form.get("GMATmoreIR")
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

#
#        #else:TOEFLmore
#
#        #data = json.loads(data)
#        #print data
#
#        if data["type"] == "1":
#            prevuniversity = data[u"prevuniversity"]
#            prevmajor = data["prevmajor"]
#            GPA = data["GPA"]
#            rank = data["rank"]
#            TOEFL = data["TOEFL"]
#            IELTS = data["IELTS"]
#            GRE  =data["GRE"]
#            GMAT = data["GMAT"]
#            description = data["description"]
#            user_id = session["user_id"]
#            User.set_user_info_detail(g.db,
#                                      user_id=user_id,
#                                      prevuniversity=prevuniversity,
#                                      prevmajor=prevmajor,
#                                      type=int(data["type"]),
#                                      description=description)
#            Score.set_user_info(g.db,university_type=1,
#                                user_id=user_id,
#                                rank=rank,
#                                TOEFL_r=int(TOEFL["r"]),
#                                TOEFL_l=int(TOEFL["l"]),
#                                TOEFL_s=int(TOEFL["s"]),
#                                TOEFL_w=int(TOEFL["w"]),
#                                IELTS_r=int(IELTS["r"]),
#                                IELTS_l=int(IELTS["l"]),
#                                IELTS_s=int(IELTS["s"]),
#                                IELTS_w=int(IELTS["w"]),
#                                GRE_v=int(GRE["v"]),
#                                GRE_q=int(GRE["q"]),
#                                GRE_aw=float(GRE["aw"]),
#                                GMAT_v=int(GMAT["v"]),
#                                GMAT_q=int(GMAT["q"]),
#                                GMAT_aw=float(GMAT["aw"]),
#                                GMAT_ir=int(GMAT["ir"])
#                                )
#        else:
#            prevuniversity = data[u"prevuniversity"]
#            prevmajor = data["prevmajor"]
#            GPA = data["GPA"]
#            rank = data["rank"]
#            TOEFL = data["TOEFL"]
#            IELTS = data["IELTS"]
#            SAT  = data["SAT"]
#            SATSUB = data["SATSUB"]
#            user_id = session["user_id"]
#            description = data["description"]
#            User.set_user_info_detail(g.db,
#                                      user_id=user_id,
#                                      prevuniversity=prevuniversity,
#                                      prevmajor=prevmajor,
#                                      type=int(data["type"]),
#                                      description=description)
#            Score.set_user_info(g.db,
#                                university_type=0,
#                                rank=rank,
#                                user_id=user_id,
#                                TOEFL_r=int(TOEFL["r"]),
#                                TOEFL_l=int(TOEFL["l"]),
#                                TOEFL_s=int(TOEFL["s"]),
#                                TOEFL_w=int(TOEFL["w"]),
#                                IELTS_r=int(IELTS["r"]),
#                                IELTS_l=int(IELTS["l"]),
#                                IELTS_s=int(IELTS["s"]),
#                                IELTS_w=int(IELTS["w"]),
#                                SAT_cr=int(SAT["cr"]),
#                                SAT_w=int(SAT["w"]),
#                                SAT_m=int(SAT["m"])
#                                )
        return jsonify(status="success")

