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
from flask import request, jsonify, g


def set_user_info():
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
            print TOEFL
            print prevuniversity
            IELTS = data["IELTS"]
            GRE  =data["GRE"]
            GMAT = data["GMAT"]
            description = data["description"]

            Score.set_user_info(g.db,university_type=1,
                                user_id=123
                                )

        # prevuniversity,prevmajor,GPA,university_type,
        # user_id,
        # rank,
        # TOEFL_r,
        # TOEFL_l,
        #
        # TOEFL_s,
        # TOEFL_w,
        # IELTS_r,
        # IELTS_l,
        # IELTS_s,
        # IELTS_w,
        # GRE_v,
        # GRE_q,
        # GRE_aw,
        # GMAT_v,
        # GMAT_q,
        # GMAT_aw,
        # GMAT_ir,
        # STA_cr,
        # STA_m,
        # STA_w
        user_id = request.args.get("user_id")
    #     print user_id
    #     user_info = map(request.args.get, (
    #         "prevuniversity","prevmajor","GPA",
    # "university_type",
    # "user_id",
    # "rank",
    # "TOEFL_r",
    # "TOEFL_l",
    #
    # "TOEFL_s",
    # "TOEFL_w",
    # "IELTS_r",
    # "IELTS_l",
    # "IELTS_s",
    # "IELTS_w",
    # "GRE_v",
    # "GRE_q",
    # "GRE_aw",
    # "GMAT_v",
    # "GMAT_q",
    # "GMAT_aw",
    # "GMAT_ir",
    # "STA_cr",
    # "STA_m"))
    #     print user_info
        data= request.get_json()
        print data
        #
        # if university_type == 1:
        #     print "asdfasdf"
        #     return 0

        return "0"

