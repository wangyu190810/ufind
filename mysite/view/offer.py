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
    get_university_twodim,set_university_offer_wechat,validate_user_login
from mysite.model.user import User
from mysite.model.major import Major
from mysite.model.state import State
from mysite.model.user_major import MajorKye
from mysite.model.faculty import Faculty

@validate_user_login
def set_offer():
    if request.method == "POST":
        data = request.form
        print data
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
            offer_major_name = data.get("offers["+str(num)+"][major_name]")
            offer_type = data.get("offers["+str(num)+"][offertype]")
            scholarship_type = data.get("offers["+str(num)+"][scholarship][type]")
            scholarship_money = data.get("offers["+str(num)+"][scholarship][money]")

            if offer_university_id is None:
                break
            num += 1
            id_major = None
            print offer_major_name
            if offer_major_name:
                print offer_major_name
                major_key = MajorKye.get_main_major(g.db,offer_major_name)
                print major_key
                if major_key:
                    faculty_id = Faculty.get_faultu_from_name(g.db,major_key.Main_Major)
                    print faculty_id
                    if faculty_id:
                        id_major = Major.add_major(g.db,name=offer_major_name,
                                        main_major=faculty_id.name,
                                        university_id=offer_university_id,
                                        faculty_id=faculty_id.id,
                                        )


            User.update_user_grade(g.db,user_id=user_id,grade=offer_grade)
            Offer.del_same_offer(g.db,university_id=offer_university_id,
                                major_id =offer_major_id,user_id=user_id)
            if id_major:
                major_id = Major.get_major_info_by_id_scalar(g.db,id_major)
                offer_major_id = id_major
            else:
                major_id = Major.get_major_info_by_id_scalar(g.db,offer_major_id)
            school1_id = 0
            school2_id = 0
            school3_id = 0
            if major_id:
                school1_id = major_id.faculty_id
                school2_id = major_id.School2_ID
                school3_id = major_id.School3_ID
            offer_num = Offer.get_offer_num(g.db,offer_university_id,user_type)
            num_wechat = 1
            if offer_num:
                if offer_num < 100:
                    num_wechat = 1
                elif 100 <= offer_num < 200:
                    num_wechat = 2
                elif 200 <= offer_num < 300:
                    num_wechat = 3

            wechat=set_university_offer_wechat(University.get_university_from_id(g.db,offer_university_id).short_name,user_type,num_wechat)
            Offer.set_offer(g.db,
                            user_id=user_id,
                            university_id=offer_university_id,
                            major_id=offer_major_id,
                            school1_id=school1_id,
                            school2_id=school2_id,
                            school3_id=school3_id,
                            user_type=user_type,
                            result=1,
                            wechat=wechat,
                            offer_type=offer_type,
                            grade=offer_grade,
                            scholarship=scholarship_money,
                            scholarship_type=scholarship_type)
            un = University.get_university_from_id(g.db, offer_university_id)
            if un:
                state_id = un.state_id
                state_offer_0 = 0
                state_offer_1 = 0
                state_offer = 0
                for row_un in University.get_state_university(g.db,state_id):
                    offer_0 = Offer.get_offer_num(g.db,row_un.id,0)
                    offer_1 = Offer.get_offer_num(g.db,row_un.id,1)
                    offer = Offer.get_offer_num(g.db,row_un.id)
                    state_offer_0 += offer_0
                    state_offer_1 += offer_1
                    state_offer += offer
                State.set_offer_num(g.db,state_id,state_offer,state_offer_0,state_offer_1)
            # 大学分数的计算
            offer_GPA = 0
            offer_GPA_0 = 0
            offer_GPA_1 = 0
            offer_TOEFL = 0
            offer_IELTS = 0
            offer_num = 0
            GPA_0_num = 0
            GPA_1_num = 0
            offer_user_list = list()
            for offer_user in Offer.get_user_id_from_university(g.db,offer_university_id):
                of_user = User.get_user_info(g.db,offer_user.user_id)

                if of_user is not None and of_user.id not in offer_user_list:

                    if of_user.GPA is not None:
                        offer_GPA += of_user.GPA
                    if of_user.TOEFL is not None:
                        offer_TOEFL += of_user.TOEFL
                    if of_user.IELTS is not None:
                        offer_IELTS += of_user.IELTS
                    if of_user:
                        if of_user.type == 0:
                            offer_GPA_0 += of_user.GPA
                            GPA_0_num += 1
                        else:
                            offer_GPA_1 += of_user.GPA
                            GPA_1_num += 1
                    offer_num += 1
                    offer_user_list.append(of_user.id)
            if offer_num == 0 or GPA_0_num == 0 or GPA_1_num == 0:
                offer_num == 1
                GPA_0_num == 1
                GPA_1_num == 1

            try:
                GPA = offer_GPA/float(offer_num)
            except ZeroDivisionError:
                GPA = 0
            try:
                GPA_0 = offer_GPA_0/float(GPA_0_num)
            except ZeroDivisionError:
                GPA_0 = 0
            try:
                GPA_1 = offer_GPA_1/float(GPA_1_num)
            except ZeroDivisionError:
                GPA_1 = 0
            try:
                TOEFL = offer_TOEFL/float(offer_num)
            except ZeroDivisionError:
                TOEFL = 0
            try:
                IELTS = offer_IELTS/float(offer_num)
            except ZeroDivisionError:
                IELTS = 0
            GPA = float("%0.2f" %GPA)
            GPA_0= float("%0.2f" %GPA_0)
            GPA_1 = float("%0.2f" %GPA_1)
            TOEFL == float("%0.2f" %TOEFL)
            IELTS = float("%0.2f" %IELTS)
            University.set_GPA_TOEFL_IELTS(g.db,offer_university_id,GPA,GPA_0,GPA_1,TOEFL,IELTS)
        offer_list = list()
        checkList = list()
        for row_user in Offer.get_offer_student_info(g.db,user_id):
            offer_dict = dict()
            offer_dict["universityid"] = row_user.university_id
            university_name = University.get_university_from_id(g.db,row_user.university_id)
            if university_name:
                offer_dict["universityname"] = university_name.chiname
                offer_dict["twodim"] = row_user.wechat
                if row_user.university_id not in checkList:
                    offer_list.append(offer_dict)
                    checkList.append(row_user.university_id)
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

