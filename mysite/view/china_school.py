# -*-coding:utf-8-*-
__author__ = 'Administrator'
# Description:

import json
from flask import request, jsonify, g, session
from mysite.model.user import User
from mysite.model.university import University
from mysite.model.faculty import Faculty
from mysite.model.major import Major
from mysite.model.compare import Compare, CompareInfo, CompareSupport
from mysite.view.base import allow_cross_domain, get_timestamp
from mysite.model.university_china import UniversityChina,SeniorHighSchool,MajorChina
from mysite.view.base import allow_cross_domain


@allow_cross_domain
def search_university_china():
    if request.method == "GET":
        search,school_type = map(request.args.get,
                                          ("name",
                                           "type"))
        print search,school_type
        if int(school_type) == 0:
            university = dict()
            search_info = list()
            print search,school_type
            for row in UniversityChina.search_university_china(g.db, search):
                print row.name
                university["name"] = row.name
                university["id"] = str(row.id)
                search_info.append(university)
                university = dict()

            return json.dumps(search_info)
        if int(school_type) == 1:
            school = dict()
            search_info = list()
            for row in SeniorHighSchool.search_senior_high(g.db,search,search):
                print row.name
                school["name"] = row.name
                school["id"] = str(row.id)
                search_info.append(school)
                school = dict()
            return json.dumps(search_info)
        error = []
    return json.dumps(error)

@allow_cross_domain
def search_major_name():
    if request.method == "GET":
        name,school_type = map(request.args.get,
                                          ("name",
                                           "type"))
        print name,school_type
        if int(school_type) == 0:
            major = dict()
            search_info = list()
            major_name = name
            faculty_name = name
            for row in MajorChina.search_major_china(g.db, faculty_name,major_name):
                print row.major_name
                major["name"] = row.major_name
                major["id"] = str(row.id)
                search_info.append(major)
                major = dict()
            return json.dumps(search_info)
        if int(school_type) == 1:
            major = dict()
            search_info = list()
            major["name"] = ""
            major["id"] = ""
            search_info.append(major)
            return json.dumps(search_info)

