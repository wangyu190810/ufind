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
from mysite.model.offer import Offer
from mysite.view.base import allow_cross_domain,get_university_img,\
    get_university_twodim
from mysite.model.user import User
from mysite.model.major import Major

@allow_cross_domain
def set_offer():
    if request.method == "POST":
        data = request.form
        user_id = session["user_id"]
        user = User.get_user_info(g.db,user_id)
        user_type = None
        if user:
            user_type = user.type

        num = 0
        while True:
            offer_major_id = data.get("offers["+str(num)+"][majorid]")
            offer_grade = data.get("offers["+str(num)+"][grade]","Bachelor")
            offer_university_id = data.get("offers["+str(num)+"][universityid]")
            offer_type = data.get("offers["+str(num)+"][offertype]")
            scholarship_type = data.get("offers["+str(num)+"][scholarship][type]")
            scholarship_money = data.get("offers["+str(num)+"][scholarship][money]")
            if offer_major_id is None:
                break
            num += 1
            User.update_user_grade(g.db,user_id=user_id,grade=offer_grade)
            Offer.del_same_offer(g.db,university_id=offer_university_id,
                                major_id =offer_major_id,user_id=user_id)
            major_id = Major.get_major_info(g.db,offer_major_id)
            school1_id = 0
            school2_id = 0
            school3_id = 0
            if major_id:
                school1_id = major_id.faculty_id
                school2_id = major_id.School2_ID
                school3_id = major_id.School3_ID
            Offer.set_offer(g.db,
                            user_id=user_id,
                            university_id=offer_university_id,
                            major_id=offer_major_id,
                            school1_id=school1_id,
                            school2_id=school2_id,
                            school3_id=school3_id,
                            user_type=user_type,
                            result=1,
                            offer_type=offer_type,
                            grade=offer_grade,
                            scholarship=scholarship_money,
                            scholarship_type=scholarship_type
            )
        offer_list = list()
        for row in Offer.get_offer_student_info(g.db,user_id):
            offer_dict = dict()
            offer_dict["universityid"] = row.university_id
            university_name= University.get_university_from_id(g.db,row.university_id)

            offer_dict["universityname"] = university_name.chiname
            offer_dict["twodim"] = get_university_twodim(university_name.name)
            if offer_dict not in offer_list:
                offer_list.append(offer_dict)
        return jsonify(status="success",
                       offerlist=offer_list,
                       description=User.get_user_info(g.db,user_id).description)

@allow_cross_domain
def get_offer_student():
    if request.method == "GET":
        user_id = session.get("user_id")
        user = User.get_user_info(g.db,user_id)
        user_type = -1
        if user:
            user_type = user.type

        university_id,major_id = map(request.args.get,("universityid","majorid"))
        student_list = []
        for row in Offer.get_offer_student(g.db,university_id,major_id,user_type):
            student_list.append(row.user_id)
        return jsonify(studentlist=student_list,
                       status="success")

