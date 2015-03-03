#! /usr/bin/python
# -*- coding:utf-8 -*-
# Filename: university.py
# Author: wangyu190810
# E-mail: wo190810401@gmail.com
# Date: 2015-01-22
# Description:

import json
from mysite.model.university import University
from flask import request,jsonify,g

from mysite.model.faculty import Faculty
from mysite.model.major import Major
from mysite.view.base import allow_cross_domain,get_university_img,get_university_logo

@allow_cross_domain
def get_university():
    if request.method == "GET":
        university_id = request.args.get("universityid")
        university = {}
        faculty = {}
        if university_id == 0:
            for university in University.get_university_info(connection=g.db):
                c = university.__dict__
            return jsonify(data=json.dumps(c), status=u"success")
        else:
            university_info = []
            faculty_info = []
            for row in University.get_university_info(g.db,university_id):
                university["name"] = row.name
                university["chiname"] = row.chiname
                university_info.append(university)

            for row in Faculty.get_faculty_info(g.db, university_id):
                faculty["name"] = row.name
                faculty["chiname"] = row.chiname
                faculty["facultyid"] = row.id
                faculty_info.append(faculty)
                faculty = {}

            return jsonify(universityinfo=university_info,
                           faculty=faculty_info,
                           status="success")


@allow_cross_domain
def get_university_info():
    if request.method == "GET":
        university_id = request.args.get("universityid")
        university_info = {}
        facultylist = []
        faculty = {}
        majorlist = []
        major = {}
        link = {}
        for row in University.get_university_info(g.db,university_id):
            university_info["universityid"] = row.id
            university_info["universitylogo"] = get_university_logo(row.name)
            link["baidu"] = row.baidu
            link["wiki"] = row.wiki
            link["official"] = row.official
            university_info["name"] = row.name
            university_info["chiname"] = row.chiname
            university_info["offernum"] = 234
            university_info["pic1"] = get_university_img(row.name,1)
            university_info["pic2"] = get_university_img(row.name,2)
            university_info["link"] = link
        for row in Faculty.get_faculty_info(g.db, university_id):
            faculty["facultyid"] = row.id
            faculty["chiname"] = row.chiname
            faculty["name"] = row.name
            for row in Major.get_major_info(g.db,
                                            university_info["universityid"],
                                            faculty["facultyid"]):
                major["majorid"] = row.id
                major["name"] = row.name
                major["pic"] = ""
                majorlist.append(major)
                major = {}
            faculty["majorlist"] = majorlist
            majorlist = []
            facultylist.append(faculty)
            faculty = {}
        university_info["facultylist"] = facultylist
        university_info["status"] = "success"
        return json.dumps(university_info)
        # return jsonify(university_info=university_info,
        #                status="success",
        #                facultylist=facultylist)



@allow_cross_domain
def get_search_university():
    if request.method == "GET":
        searchname, stateid = map(request.args.get,("searchname","stateid"))
        universitylist = []
        university = {}
        if stateid is None:

            for row in University.search_university(g.db,searchname):
                university["name"] = row.name
                university["chiname"] = row.chiname
                university["id"] = row.id
                university["logo"] = row.schoollogo
                universitylist.append(university)
                university = {}
            return jsonify(namelist=universitylist,
                           stattus="success")
        else:
            for row in University.search_university(g.db,searchname,stateid):
                university["name"] = row.name
                university["chiname"] = row.chiname
                university["id"] = row.id
                university["logo"] = row.schoollogo
                universitylist.append(university)
                university = {}
            return jsonify(namelist=universitylist,
                           stattus="success")
@allow_cross_domain
def get_university_list():
    if request.method == "GET":
        name = []
        for row in University.university_name_list(g.db):
            name.append(row.name)
        return jsonify(university=name)


@allow_cross_domain
def get_state_university():
    if request.method == "GET":
        university = {}
        state_id = request.args.get("stateid")
        university["statepic"] = ""
        universitylist = []
        university_info = {}
        for row in University.get_state_university(g.db,state_id):
            university_info["name"] = row.name
            university_info["chiname"] = row.chiname
            university_info["universityid"] = row.id
            university_info["universitypic"] = "school1.jpg"
            university_info["latitude"] = row.latitude
            university_info["longitude"] = row.longitude
            university_info["offernum"] = "12"
            university_info["meanGPA"] = "32"
            university_info["meanTOEFL"] = "123"
            universitylist.append(university_info)
            university_info = {}
        university["universitylist"] = universitylist
        university["status"] = "success"
        return json.dumps(university)