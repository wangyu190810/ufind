#! /usr/bin/python
#-*- coding:utf-8 -*-
#Filename: university.py
#Author: wangyu190810
#E-mail: wo190810401@gmail.com
#Date: 2015-01-22
#Description: 

import json
from mysite.model.university import University
from mysite.model.faculty import Faculty
from mysite.model.major import Major
from flask import request,jsonify,g
from mysite.model.compare import CompareInfo

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
            return jsonify(namelist=major_list,status="success")
        else:
            for row in Major.search_maior(g.db, searchname, university_id):
                major["name"] = row.name
                major["chiname"] = row.chiname
                major["id"] = row.id
                major_list.append(major)
            return jsonify(namelist=major_list,status="success")

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



