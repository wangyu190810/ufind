# -*-coding: utf-8-*-

__author__ = 'wangyu'

import json

from flask import request, g

from mysite.model.university_china import UniversityChina, SeniorHighSchool,\
    MajorChina
from mysite.view.base import allow_cross_domain


@allow_cross_domain
def search_university_china():
    if request.method == "GET":
        search, school_type = map(request.args.get, ("name", "type"))
        if int(school_type) == 1:
            university = dict()
            search_info = list()
            for row in UniversityChina.search_university_china(g.db, search):
                university["name"] = row.name
                university["id"] = str(row.id)
                search_info.append(university)
                university = dict()

            return json.dumps(search_info)
        if int(school_type) == 0:
            school = dict()
            search_info = list()
            for row in SeniorHighSchool.search_senior_high(g.db, search,
                                                           search):
                school["name"] = row.name
                school["id"] = str(row.id)
                search_info.append(school)
                school = dict()
            return json.dumps(search_info)
    return json.dumps({"static": "success"})


@allow_cross_domain
def search_major_name():
    if request.method == "GET":
        name, school_type = map(request.args.get, ("name", "type"))
        if int(school_type) == 1:
            major = dict()
            search_info = list()
            major_name = name
            faculty_name = name
            for row in MajorChina.search_major_china(g.db, faculty_name,
                                                     major_name):
                major["name"] = row.major_name
                major["id"] = str(row.id)
                search_info.append(major)
                major = dict()
            return json.dumps(search_info)
        if int(school_type) == 0:
            major = dict()
            search_info = list()
            major["name"] = u"文科"
            major["id"] = 1
            search_info.append(major)
            major = dict()
            major["name"] = u"理科"
            major["id"] = 2
            search_info.append(major)
            major = dict()
            major["name"] = u"其他"
            major["id"] = 3
            search_info.append(major)
            return json.dumps(search_info)
    return json.dumps({"static": "success"})
