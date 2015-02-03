#! /usr/bin/python
#-*- coding:utf-8 -*-
#Filename: university.py
#Author: wangyu190810
#E-mail: wo190810401@gmail.com
#Date: 2015-01-22
#Description: 

import json
from flask import request,jsonify,g,session
from mysite.model.user import User
from mysite.model.university import University
from mysite.model.faculty import Faculty
from mysite.model.major import Major
from mysite.model.compare import Compare, CompareInfo,CompareSupport
from mysite.view.base import allow_cross_domain,get_timestamp

@allow_cross_domain
def set_compare():
    if request.method == "POST":

        data = json.loads(request.data)
        print data
        comparelist = data["comparelist"]
        print data
        print comparelist
        description = data["description"]
        print session
        user_id = session["user_id"]
        Compare.set_compare(connection=g.db,user_id=user_id,description=description)
        compare_id = Compare.get_compare_id(g.db)
        for row in comparelist:
            university_id = int(row["universityid"])
            major_id = int(row["majorid"])
            CompareInfo.set_compare_info(g.db,
                                        compare_id=compare_id,
                                        university_id=university_id,
                                        major_id=major_id)
        return jsonify(status="success")


@allow_cross_domain
def get_compare():
    if request.method == "GET":
        compareid = request.args.get("compareid")
        compare = {}
        compare_info = {}
        comparelist = []
        for row in Compare.get_compare(g.db,compareid):
            compare["compareid"] = row.id
            compare["description"] = row.description
            compare["date"] = get_timestamp(row.create_time)
            compare["studentid"] = row.user_id
            #compare["major_id"] = row.major_id
            print compareid
        for row in CompareInfo.get_compare_info(g.db,compareid):
            compare_info["universityid"] = row.university_id
            compare_info["major_id"] = row.major_id
            compare_info["supportnum"] = row.supportnum
            for university in University.get_university_info(g.db,
                                                      university_id=row.university_id):
                compare_info["universityname"] = university.name
                compare_info["logo"] = university.schoollogo
            for major in Major.get_major_info(g.db,
                                            university_id=compare_info["universityid"],
                                            major_id = compare_info["major_id"]):
                compare_info["majorname"] = major.name
            compare_info["offernum"] = 12312
            comparelist.append(compare_info)

            compare_info = {}
        compare["comparelist"] =comparelist
        compare["status"] = "success"
        return json.dumps(compare)


def set_compare_support():
    if request.method == "POST":
        data = json.loads(request.data)
        user_id = session["user_id"]
        compare_info_id = data["compareinfoid"]
        CompareSupport.set_compare_support(g.db,user_id,compare_info_id)
        return jsonify(status="success")


def get_compare_list():
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
        for row in CompareInfo.get_compare_university_major(g.db,university_id,major_id):
            compare_list.append(str(row.compare_id))

        return jsonify(compares=compare_list,
                       status="success")


