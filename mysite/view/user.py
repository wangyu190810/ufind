# -*-coding:utf-8-*-
__author__ = 'wangyu'

from flask import g, jsonify, request
import json

from mysite.model.user import User



def get_user_info(studentid):
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

