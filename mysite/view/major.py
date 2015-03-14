#! /usr/bin/python
#-*- coding:utf-8 -*-
#Filename: university.py
#Author: wangyu190810
#E-mail: wo190810401@gmail.com
#Date: 2015-01-22
#Description: 

import json
from flask import request,jsonify,g
from mysite.model.university import University
from mysite.model.faculty import Faculty
from mysite.model.major import Major
from mysite.model.compare import CompareInfo
from mysite.view.base import allow_cross_domain
from mysite.model.offer import Offer
from mysite.model.user import User

@allow_cross_domain
def search_major():
    """专业搜索"""
    if request.method == "GET":
        major_list = []
        major = {}
        searchname,university_id = map(request.args.get,("searchname","universityid"))
        if university_id is None:
            for row in  Major.search_maior(g.db, searchname):
                major["name"] = row.name
                major["chiname"] = row.chiname
                major["id"] = row.id
                major_list.append(major)
                major = {}
            return jsonify(namelist=major_list,status="success")
        else:
            for row in Major.search_maior(g.db, searchname, university_id):
                major["name"] = row.name
                major["chiname"] = row.chiname
                major["id"] = row.id
                major_list.append(major)
                major = {}
            return jsonify(namelist=major_list,status="success")


@allow_cross_domain
def get_major_compare():
    """返回投票信息"""
    if request.method == "GET":
        university_id, major_id = map(request.args.get,("universityid","majorid"))
        compare_id = []
        print university_id,major_id
        for row in CompareInfo.get_compare_random(g.db,university_id,major_id):
            compare_id.append(str(row.compare_id))

        return jsonify(compareid=compare_id,
                        status=u"success")


@allow_cross_domain
def get_major_from_university_faculty():
    """投票根据学校和学院返回专业信息"""
    if request.method == "GET":
        university_id,faculty_id = map(request.args.get, ("universityid",
                                                          "facultyid"))
        major_list = []
        major_info = {}
        if faculty_id is None:
            for row in Major.get_major_info(g.db,university_id):
                students = list()
                major_info["majorid"] = row.id
                major_info["name"] = row.name
                major_info["offernum"] = Offer.get_offer_student(g.db,
                                                                 university_id,
                                                                 row.id)
                major_info["offervote"]=None
                offervote = dict()
                for row_major in Offer.get_user_id_from_major(g.db,row.id):
                    student_info = dict()
                    user = User.get_user_info(g.db,row_major.user_id)
                    student_info["studentid"] = user.id
                    student_info["name"] = user.username
                    student_info["GPA"] = user.gpa
                    student_info["prevuniversity"] = user.prevuniversity
                    students.append(student_info)
                major_info["students"] = students
            return jsonify(status="success",
                           majorlist=major_info)
        else:
            for row in Major.get_major_info(g.db,university_id,faculty_id):
                students = list()
                major_info["majorid"] = row.id
                major_info["name"] = row.name
                major_info["offernum"] = Offer.get_offer_student(g.db,
                                                                 university_id,
                                                                 row.id)
                major_info["offervote"]=None
                for row_major in Offer.get_user_id_from_major(g.db,row.id):
                    student_info = dict()
                    user = User.get_user_info(g.db,row_major.user_id)
                    student_info["studentid"] = user.id
                    student_info["name"] = user.username
                    student_info["GPA"] = user.gpa
                    student_info["prevuniversity"] = user.prevuniversity
                    students.append(student_info)
                major_info["students"] = students
            return jsonify(status="success",
                           majorlist=major_info)



#
#
#           for row_un in University.get_university_info(g.db,university_id):
#                    pass
#
#                for major_row in CompareInfo.get_compare_about_major(g.db,row.id):
#                    for compare_row in CompareInfo.get_compare_info(g.db,major_row.id):
#                        for university_row in University.get_university_info(g.db,compare_row.university_id):
#                            offervote["compuniversityid"] = compare_row.university_id
#                            offervote["compname"] = university_row.name
#                            offervote["compmajor"] = university_row.major
#

