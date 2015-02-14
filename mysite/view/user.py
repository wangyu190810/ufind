# -*-coding:utf-8-*-
__author__ = 'wangyu'

from flask import g, jsonify, request,redirect,session
import json

from mysite.model.user import User
from mysite.view.base import allow_cross_domain
from mysite.model.offer import Offer
from mysite.model.university import University
from mysite.model.major import Major
from mysite.model.compare import CompareInfo,Compare


@allow_cross_domain
def get_user_info():
    if request.method == "GET":
        studentid = request.args.get("studentid")
        student_info = {}
        for row in User.get_user_info(g.db,studentid):
            student_info["prevuniversity"] = row.prevuniversity
            student_info["name"] = row.username
            student_info["prevmajor"] = row.prevmajor
            student_info["GPA"] = row.GPA
            student_info["TOEFL"] =row.TOEFL
            student_info["IELTS"] = row.IELTS
            student_info["GMAT"] = row.GMAT
            student_info["SAT"] = row.SAT
            student_info["pic"] = row.pic
        universityname = []
        student_info["universityname"] = universityname
        return json.dumps(student_info)

@allow_cross_domain
def get_user_detail_info():
    if request.method == "GET":
        studentid = request.args.get("studentid")
        print studentid
        student_info = {}
        student_info["fannum"] = 123
        offers = []
        offer_info = {}
        for row in Offer.get_offer_student_info(g.db,
                                       studentid):
            for row_un in University.get_university_info(g.db,row.university_id):
                offer_info["universityname"] = row_un.name
                offer_info["logo"] = row_un.schoollogo
            for row_ma in Major.get_major_info_by_id(g.db,row.major_id):
                offer_info["majorname"] = row_ma.name
            offer_info["twodimcode"] = ""
            offers.append(offer_info)
        student_info["offers"] = offers
        compares = []
        compares_info = {}
        for row_co in Compare.get_compare_user_id(g.db,studentid):
            compares_info["compareid"] = row_co.id
            compareslist = []
            compares_un = {}
            for row_ci in CompareInfo.get_compare_info(g.db,row_co.id):
                for row_un in University.get_university_info(g.db,row_ci.university_id):
                    compares_un["universityname"] = row_un.name
                    compares_un["universityid"] = row_un.id
                    compares_un["logo"] = row_un.schoollogo
                for row_ma in CompareInfo.get_compare_info(g.db,row_ci.major_id):
                    compares_un["majorname"] = row_ma.name
                    compares_un["supportnum"] = row_ci.supportnum
                #for row_of in  Offer.get_offer_num(g.db,row_ci.university_id):
                compares_un["offernum"] = Offer.get_offer_num(g.db,row_ci.university_id)
                #    compares_un["offernum"] = row_of.count
                #    print row_of.count
                print compares_un["offernum"]
                compareslist.append(compares_un)
                compares_un = {}
            compares_info["comparelist"] = compareslist
            compares.append(compares_info)
        student_info["compares"] = compares
        for row_us in User.get_user_info(g.db,studentid):
            student_info["description"] = row_us.description

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
        page =data["page"]
        compares = {}
        compare_list = []
        page_list = []
        student_list = []
        student = {}
        if faculty_id == "":
            if major_id == "":
                major_id = None
            for row in Offer.get_user_id_from_university(g.db,int(university_id),int(major_id)):
                student_list.append(str(row.user_id))
                student["studentlist"] = student_list
                page = len(student_list)/15
            student["more"] = ""
            if int(page) > 1:
                student["more"] = "true"
            student["status"] = "success"

            return json.dumps(student)

        return jsonify(status="123")


