<<<<<<< HEAD:mysite/view/major.py
#! /usr/bin/python
<<<<<<< HEAD:views/major.py
# -*-coding:utf-8-*-
=======
# coding: utf-8
# email: khahux@163.com

>>>>>>> 906fe4c29000ededa1036345f7ffa9361e383900:views/major.py
=======

>>>>>>> fixbug:mysite/view/major.py
from flask import request, jsonify, g

from models.user import User
from models.major import Major
from models.offer import Offer
from models.compare import CompareInfo

from lib.decorators import allow_cross_domain


@allow_cross_domain
def search_major():
    u"""专业搜索"""
    if request.method == "GET":
        major_list = []
        major = {}
        searchname, university_id = map(request.args.get, ("searchname", "universityid"))

        if university_id is None:
            for row in Major.search_maior(g.db, searchname):
                major["name"] = row.name
                major["chiname"] = row.chiname
                major["id"] = row.id
                major_list.append(major)
                major = {}
            return jsonify(namelist=major_list,
                           status="success")
        else:
            for row in Major.search_maior(g.db, searchname, university_id):
                major["name"] = row.name
                major["chiname"] = row.chiname
                major["id"] = row.id
                major_list.append(major)
                major = {}
            return jsonify(namelist=major_list,
                           status="success")


@allow_cross_domain
def get_major_compare():
    u"""返回投票信息"""
    if request.method == "GET":
        university_id, major_id = map(request.args.get,
                                      ("universityid", "majorid"))
        compare_id = []
        for row in CompareInfo.get_compare_random(g.db,
                                                  university_id,
                                                  major_id):
            compare_id.append(str(row.compare_id))

        return jsonify(compareid=compare_id,
                       status="success")


@allow_cross_domain
def get_major_from_university_faculty():
    u"""投票根据学校和学院返回专业信息"""
    if request.method == "GET":
        university_id, faculty_id, major_id = map(request.args.get, ("universityid",
                                                                     "facultyid",
                                                                     "majorid"))

        major_list = list()
        if faculty_id is None and major_id is None:
            for row in Major.get_major_info_university(g.db, university_id):
                students = list()
                major_info = dict()
                major_info["majorid"] = row.id
                major_info["name"] = row.name
                major_info["offernum"] = Offer.get_offer_num_from_major(g.db, university_id, row.id)
                major_info["offervote"] = None
                # offervote = dict()
                for row_major in Offer.get_user_id_from_major(g.db, row.id):
                    student_info = dict()
                    user = User.get_user_info(g.db, row_major.user_id)
                    if user is None:
                        students.append(student_info)
                    else:
                        student_info["studentid"] = user.id
                        student_info["studentimg"] = user.pic
                        student_info["name"] = user.username
                        student_info["GPA"] = user.GPA
                        student_info["prevuniversity"] = user.prevuniversity

                        students.append(student_info)
                    major_info["students"] = students
                if major_info.get("students") is not None:
                    major_list.append(major_info)
                print "zxcvzxcvzvc"
            return jsonify(status="success",
                           majorlist=major_list)
        elif major_id is None:
            faculty_list = faculty_id.split(",")
            for faculty_id in faculty_list:
                for row in Major.get_major_info(g.db, university_id, faculty_id):
                    students = list()
                    major_info = {}
                    major_info["majorid"] = row.id
                    major_info["name"] = row.name
#                major_info["offernum"] = Offer.get_offer_num(g.db,
#                                                                 university_id,)
                    major_info["offernum"] = Offer.get_offer_num_from_major(g.db, university_id, row.id)
                    major_info["offervote"] = None
                    for row_major in Offer.get_user_id_from_major(g.db, row.id):
                        student_info = dict()
                        user = User.get_user_info(g.db, row_major.user_id)
                        student_info["studentid"] = user.id
                        student_info["name"] = user.username
                        student_info["studentimg"] = user.pic
                        student_info["GPA"] = user.GPA
                        student_info["prevuniversity"] = user.prevuniversity
                        students.append(student_info)
                        major_info["students"] = students
                    if major_info.get("students") is not None:
                        major_list.append(major_info)
            return jsonify(status="success",
                           majorlist=major_list)
        elif major_id is not None:
            students = list()
            for row in Major.get_major_info(g.db, university_id=university_id, major_id=major_id):
                major_info = dict()
                major_info["majorid"] = row.id
                major_info["name"] = row.name
#               or_info["offernum"] = Offer.get_offer_num(g.db,
#                                                         university_id,)
                major_info["offernum"] = Offer.get_offer_num_from_major(g.db, university_id, row.id)
                major_info["offervote"] = None
                for row_major in Offer.get_user_id_from_major(g.db, row.id):
                    student_info = dict()
                    user = User.get_user_info(g.db, row_major.user_id)
                    student_info["studentid"] = user.id
                    student_info["name"] = user.username
                    student_info["studentimg"] = user.pic
                    student_info["GPA"] = user.GPA
                    student_info["prevuniversity"] = user.prevuniversity
                    students.append(student_info)
                    major_info["students"] = students
                print "123123123"
                if major_info.get("students") is not None:
                    major_list.append(major_info)
            return jsonify(status="success",
                           majorlist=major_list)
