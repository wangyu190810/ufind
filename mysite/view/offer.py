#! /usr/bin/python
#-*- coding:utf-8 -*-
#Filename: university.py
#Author: wangyu190810
#E-mail: wo190810401@gmail.com
#Date: 2015-01-22
#Description: 

import json
from flask import request,jsonify,g,session
from mysite.model.university import University
from mysite.model.faculty import Faculty
from mysite.model.major import Major
from mysite.model.offer import Offer
from mysite.view.base import allow_cross_domain


@allow_cross_domain
def set_offer():
    if request.method == "POST":
        data = request.form

        user_id = session["user_id"]
        num = 0
        while True:
            offer_major_id = data.get("offers[0][majorid]")
            if offer_major_id is None:
                break

#        for row in offer:
#            university_id = int(row["universityid"])
#            major_id = int(row["majorid"])
#            result = int(row["result"])
#            Offer.set_offer(g.db,
#                            user_id=user_id,
#                            university_id=university_id,
#                            major_id=major_id,
#                            result=result)

        return jsonify(status="success",
                       img="asdfsda")

@allow_cross_domain
def get_offer_student():
    if request.method == "GET":
        university_id,major_id = map(request.args.get,("universityid","majorid"))
        student_list = []
        for row in Offer.get_offer_student(g.db,university_id,major_id):
            student_list.append(row.id)
        return jsonify(studentlist=student_list,
                       status="success")

