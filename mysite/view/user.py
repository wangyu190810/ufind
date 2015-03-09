# -*-coding:utf-8-*-
__author__ = 'wangyu'

from flask import g, jsonify, request, session
import json

from mysite.model.user import User,UserFollow
from mysite.view.base import allow_cross_domain,get_timestamp
from mysite.model.offer import Offer
from mysite.model.university import University
from mysite.model.major import Major
from mysite.model.compare import CompareInfo, Compare
from mysite.model.message import Message


@allow_cross_domain
def get_user_info():
    if request.method == "GET":
        print request.args
        student_id = request.args.get("studentid")
        student_info = {}
        row = User.get_user_info(g.db, student_id)
        student_info["prevuniversity"] = row.prevuniversity
        student_info["name"] = row.username
        student_info["prevmajor"] = row.prevmajor
        student_info["GPA"] = row.GPA
        student_info["TOEFL"] = row.TOEFL
        student_info["IELTS"] = row.IELTS
        student_info["GMAT"] = row.GMAT
        student_info["SAT"] = row.SAT
        student_info["pic"] = row.pic
        universityname = []
        student_info["universityname"] = universityname
        student_info["status"] = "success"
        return json.dumps(student_info)
    return jsonify(status="false")


@allow_cross_domain
def get_user_detail_info():
    if request.method == "GET":
        student_id = request.args.get("studentid")
        student_info = dict()
        offers = list()
        login_user_id = session.get("user_id")
        if login_user_id is None:
            login_user_id = -1
        for row in Offer.get_offer_student_info(g.db,student_id):
            offer_info = dict()
            for row_un in University.get_university_info(g.db,
                                                         row.university_id):
                offer_info["universityname"] = row_un.name
                offer_info["logo"] = row_un.schoollogo
            for row_ma in Major.get_major_info_by_id(g.db, row.major_id):
                offer_info["majorname"] = row_ma.name
            offer_info["twodimcode"] = ""
            offer_info["grade"] = row.grade
            offer_info["offertype"] = row.offer_type
            if row.scholarship is not None:
                offer_info["scholarship"] = str(row.scholarship)+\
                                            row.scholarship_type
            else:
                offer_info["scholarship"] = None
            offers.append(offer_info)
        student_info["offers"] = offers
        compares = []
        compares_info = {}
        for row_co in Compare.get_compare_user_id(g.db, student_id):
            compares_info["compareid"] = row_co.id
            compareslist = list()
            compares_un = {}
            for row_ci in CompareInfo.get_compare_info(g.db, row_co.id):
                for row_un in University.get_university_info(g.db,
                                                             row_ci.university_id):
                    compares_un["universityname"] = row_un.name
                    compares_un["universityid"] = row_un.id
                    compares_un["logo"] = row_un.schoollogo
                for row_ma in CompareInfo.get_compare_info(g.db,
                                                           row_ci.major_id):
                    compares_un["majorname"] = row_ma.name
                    compares_un["supportnum"] = row_ci.supportnum
                # for row_of in  Offer.get_offer_num(g.db,row_ci.university_id):
                compares_un["offernum"] = Offer.get_offer_num(g.db,
                                                              row_ci.university_id)
                #    compares_un["offernum"] = row_of.count
                #    print row_of.count
                print compares_un["offernum"]
                compareslist.append(compares_un)
                compares_un = {}
            compares_info["comparelist"] = compareslist
            compares.append(compares_info)
        student_info["compares"] = compares
        user = User.get_user_info(g.db, student_id)
        print user
        print type(user)
        student_info["fannum"] = UserFollow.get_follow_count_user(g.db,student_id)
        if user is None:
            student_info["description"] = ""
            student_info["bginf"] = ""
        else:
            student_info["description"] = user.description
            student_info["bginf"] = user.bginf
        if int(login_user_id) == int(student_id):
            student_info["self"] = "true"
            student_info["phone"] = user.phone
            student_info["email"] = user.email
        else:
            student_info["self"] = "false"
            student_info["phone"] = ""
            student_info["email"] = ""

        message = list()
        for row_meg in Message.get_message_user(g.db,student_id):
            message_dict = dict()
            message_dict["messageid"] = row_meg.id
            user_id = row_meg.user_id
            user = User.get_user_info(g.db,user_id)
            message_dict["pic"] = user.pic
            message_dict["name"] = user.username
            message_dict["studentid"] = user_id
            message_dict["content"] = row_meg.message
            message_dict["time"] = get_timestamp(row_meg.create_time)
            message.append(message_dict)
        student_info["messages"] = message

        follow_status = UserFollow.get_follow_to_user(g.db,student_id,login_user_id)
        if follow_status is not None:
            student_info["followed"] = "true"
        else:
            student_info["followed"] = "false"
        follows_list = list()
        for row_follow in UserFollow.get_follow_id(g.db,student_id):
            follows = dict()
            follow_user_id = row_follow.follow_user_id
            user = User.get_user_info(g.db,follow_user_id)
            follows["name"] = user.username
            follows["pic"] = user.pic
            follows["studentid"] = user_id
            follows_list.append(follows)
        student_info["follows"] = follows_list
        student_info["status"] = "success"

        return json.dumps(student_info)


@allow_cross_domain
def get_user_in_university():
    if request.method == "POST":
        data = json.loads(request.data)
        university_id = data["universityid"]
        faculty_id = data["facultyid"]
        major_id = data["majorid"]
        grade = data["grade"]
        GPA = data["GPA"]
        TOEFL = data["TOEFL"]
        GRE = data["GRE"]
        IELTS = data["IELTS"]
        GMAT = data["GMAT"]
        SAT = data["SAT"]
        page = data["page"]
        compares = {}
        compare_list = []
        page_list = []
        student_list = []
        student = {}
        if faculty_id == "":
            if major_id == "":
                major_id = None
            for row in Offer.get_user_id_from_university(g.db,
                                                         int(university_id),
                                                         int(major_id)):
                student_list.append(str(row.user_id))
                student["studentlist"] = student_list
                page = len(student_list) / 15
            student["more"] = ""
            if int(page) > 1:
                student["more"] = "true"
            student["status"] = "success"

            return json.dumps(student)

        return jsonify(status="123")


def update_user_bginf():
    """修改个人背景信息"""
    if request.method == "POST":
        bginf = request.form.get("bginf")
        user_id = session.get("user_id")
        User.update_user_bginf(g.db, user_id=user_id, bginf=bginf)
        return jsonify(status="success")
    return jsonify(status="false")


