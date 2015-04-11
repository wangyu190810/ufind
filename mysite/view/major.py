#! /usr/bin/python
# -*-coding:utf-8-*-
from flask import request, jsonify, g,session
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
        user_id = session.get("user_id")
        user = User.get_user_info(g.db,user_id)
        major_type = None
        if user:
            major_type = user.type
        searchname,university_id = map(request.args.get,
                                       ("searchname", "universityid"))

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
            for row in Major.search_maior(g.db, searchname, university_id,major_type):
                major["name"] = row.name
                major["chiname"] = row.chiname
                major["id"] = row.id
                major_list.append(major)
                major = {}
            return jsonify(namelist=major_list,
                           status="success")


@allow_cross_domain
def get_major_compare():
    """返回投票信息"""
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
    """投票根据学校和学院返回专业信息"""
    if request.method == "GET":
        user = User.get_user_info(g.db,user_id=session.get("user_id"))
        university_id,faculty_id,major_id = map(request.args.get,
                                                ("universityid",
                                                "facultyid",
                                                "majorid"))



        user_type = None
        if user:
            user_type = user.type
        major_list = list()
        if faculty_id is None and major_id is None:
            for row in Major.get_major_info_university(g.db, university_id):
                students = list()
                major_info = dict()
                major_info["majorid"] = row.id
                major_info["name"] = row.name
                major_info["offernum"] = Offer.get_offer_num_from_major(g.db,university_id,row.id)
                major_info["offervote"]= None
                #offervote = dict()
                for row_major in Offer.get_user_id_from_major(g.db,row.id,user_type):
                    student_info = dict()
                    user = User.get_user_info(g.db,row_major.user_id)
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
            return jsonify(status="success",
                           majorlist=major_list)
        elif major_id is None:
            faculty_list = faculty_id.split(",")
            for faculty_id in faculty_list:
                for row in Major.get_major_info(connection=g.db,university_id=university_id,faculty_id=faculty_id):
                    students = list()
                    major_info = {}
                    major_info["majorid"] = row.id
                    major_info["name"] = row.name
#                major_info["offernum"] = Offer.get_offer_num(g.db,
#                                                                 university_id,)
                    major_info["offernum"] = Offer.get_offer_num_from_major(g.db,university_id,row.id)
                    major_info["offervote"]=None
                    for row_major in Offer.get_user_id_from_major(g.db,row.id,user_type):
                        student_info = dict()
                        user = User.get_user_info(g.db,row_major.user_id)
                        if user is None:
                            students.append(student_info)
                        else:
                            students.append(student_info)
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
            for row in Major.get_major_info(g.db,university_id=university_id,major_id=major_id):
                major_info = dict()
                major_info["majorid"] = row.id
                major_info["name"] = row.name
#               or_info["offernum"] = Offer.get_offer_num(g.db,
#                                                         university_id,)
                major_info["offernum"] = Offer.get_offer_num_from_major(g.db,university_id,row.id)
                major_info["offervote"]=None
                for row_major in Offer.get_user_id_from_major(g.db,row.id,user_type):
                    student_info = dict()
                    user = User.get_user_info(g.db,row_major.user_id)
                    if user:
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


