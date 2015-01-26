#! /usr/bin/python
#-*- coding:utf-8 -*-
#Filename: university.py
#Author: wangyu190810
#E-mail: wo190810401@gmail.com
#Date: 2015-01-22
#Description: 

import json
from mysite.model.university import University
#from mysite.model.major import
from mysite.model.faculty import Faculty
from mysite.model.major import Major
from flask import request,jsonify,g


def get_university(university_id):
    if request.method == "GET":
        university = {}
        faculty = {}
        if university_id == 0:
            for university in University.get_university_info(connection=g.db):
                c =  university.__dict__
            data= json.dumps(c)
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
                faculty_info.append(faculty)


            return jsonify(universityinfo=university_info,
                           faculty=faculty_info,
                           stattus="success")


def get_university_info(university_id):
    if request.method == "GET":
        university_info = {}
        facultylist = []
        faculty = {}
        majorlist = []
        major = {}
        link = {}
        for row in University.get_university_info(g.db,university_id):
            university_info["universityid"] = row.id
            university_info["universitylogo"] = row.id
            link["baidu"] = row.baidu
            link["wiki"] = row.wiki
            link["official"] = row.official
            university_info["name"] = row.name
            university_info["chiname"] = row.name
            university_info["offrnum"] = 234
            university_info["pic1"] = "pic1"
            university_info["pic2"] = "pic2"
        for row in Faculty.get_faculty_info(g.db, university_id):
            faculty["facultyid"] = row.id
            print row.id
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
        return jsonify(university_info=university_info,
                       status="success",
                       facultylist=facultylist)




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
                universitylist.append(university)
                
            return jsonify(namelist=universitylist,
                           stattus="success")
        else:
            for row in University.search_university(g.db,searchname,stateid):
                university["name"] = row.name
                university["chiname"] = row.chiname
                university["id"] = row.id
                universitylist.append(university)
            return jsonify(namelist=universitylist,
                           stattus="success")



