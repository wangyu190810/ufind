#! /usr/bin/python
# -*- coding:utf-8 -*-
#Filename: university.py
#Author: wangyu190810
#E-mail: wo190810401@gmail.com
#Date: 2015-01-22
#Description:

import json
from mysite.model.university import University
from mysite.model.faculty import Faculty
from mysite.model.major import Major
from mysite.model.score import Score
from flask import request, jsonify, g ,session


def set_user_info():
    print request.data
    if request.method == "POST":
        data = request.data
        data = json.loads(data)
        print data
        if data["type"] == "1":
            prevuniversity = data[u"prevuniversity"]
            prevmajor = data["prevmajor"]
            GPA = data["GPA"]
            rank = data["rank"]
            TOEFL = data["TOEFL"]
            IELTS = data["IELTS"]
            GRE  =data["GRE"]
            GMAT = data["GMAT"]
            description = data["description"]
            user_id = session["user_id"]
            Score.set_user_info(g.db,university_type=1,
                                user_id=user_id,
                                rank=rank,
                                TOEFL_r=int(TOEFL["r"]),
                                TOEFL_l=int(TOEFL["l"]),
                                TOEFL_s=int(TOEFL["s"]),
                                TOEFL_w=int(TOEFL["w"]),
                                IELTS_r=int(IELTS["r"]),
                                IELTS_l=int(IELTS["l"]),
                                IELTS_s=int(IELTS["s"]),
                                IELTS_w=int(IELTS["w"]),
                                GRE_v=int(GRE["v"]),
                                GRE_q=int(GRE["q"]),
                                GRE_aw=int(GRE["aw"]),
                                GMAT_v=int(GMAT["v"]),
                                GMAT_q=int(GMAT["q"]),
                                GMAT_aw=int(GMAT["aw"]),
                                GMAT_ir=int(GMAT["ir"])
                                )
        else:
            prevuniversity = data[u"prevuniversity"]
            prevmajor = data["prevmajor"]
            GPA = data["GPA"]
            rank = data["rank"]
            TOEFL = data["TOEFL"]
            IELTS = data["IELTS"]
            SAT  = data["SAT"]
            SATSUB = data["SATSUB"]
            user_id = session["session"]
            description = data["description"]
            Score.set_user_info(g.db,
                                university_type=0,
                                rank=rank,
                                user_id=user_id,
                                TOEFL_r=int(TOEFL["r"]),
                                TOEFL_l=int(TOEFL["l"]),
                                TOEFL_s=int(TOEFL["s"]),
                                TOEFL_w=int(TOEFL["w"]),
                                IELTS_r=int(IELTS["r"]),
                                IELTS_l=int(IELTS["l"]),
                                IELTS_s=int(IELTS["s"]),
                                IELTS_w=int(IELTS["w"]),
                                SAT_cr=int(SAT["cr"]),
                                SAT_w=int(SAT["w"]),
                                SAT_m=int(SAT["m"])
                                )

        data = request.get_json()

        return jsonify(status="success")

