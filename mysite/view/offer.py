#! /usr/bin/python
# -*- coding:utf-8 -*-
# Filename: university.py
# Author: 22too
# E-mail: wo190810401@gmail.com
# Date: 2015-01-22
# Description:


from flask import request,jsonify,g,session
from mysite.model.university import University
from mysite.model.offer import Offer
from mysite.view.base import allow_cross_domain,get_university_img,\
    get_university_twodim
from mysite.model.user import User


@allow_cross_domain
def set_offer():
    if request.method == "POST":
        data = request.form
        user_id = session["user_id"]
        num = 0
        user = User.get_user_info(g.db,user_id)
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
            Offer.set_offer(g.db,
                            user_id=user_id,
                            university_id=offer_university_id,
                            major_id=offer_major_id,
                            result=1,
                            offer_type=offer_type,
                            grade=offer_grade,
                            scholarship=scholarship_money,
                            scholarship_type=scholarship_type)
            for offer_user in Offer.get_user_id_from_university(g.db,
                                                                university_id=offer_university_id):
                offer_user.user_id
            if user is not None:
                University.update_university_GPA_TOEFL(g.db,
                                                       university_id=
                                                       offer_university_id,
                                                       GPA=user.GPA,
                                                       TOEFL=user.TOEFL)
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
        university_id,major_id = map(request.args.get,("universityid","majorid"))
        student_list = []
        for row in Offer.get_offer_student(g.db,university_id,major_id):
            student_list.append(row.user_id)
        return jsonify(studentlist=student_list,
                       status="success")

