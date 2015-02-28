__author__ = 'wangyu'
from flask import render_template,redirect,g,session,request,jsonify
from mysite.view.base import allow_cross_domain
from mysite.model.user import User

import json

@allow_cross_domain
def login():
    data = request.form
    email = data["email"]
    password = data["password"]
    user = User.login_user(g.db,email,password)
    if user is not None:
        print user
        session["user_id"] = user.id
        student = {}
        student["studentid"] = user.id
        student["studentname"] = user.username
        student["studentpic"] = user.pic
        return jsonify(status="success",
                       student=student
                       )
    return jsonify(status="false")

@allow_cross_domain
def register_first():
    if request.method == "POST":
        print request.data
        data = request.form
        print data
        email  = data["email"]
        passwrod = data["password"]
        phonenum = data["phonenum"]
        checknum = data["checknum"]
        check = User.get_checknum(g.db,phonenum)
        if check is None:
            print "12"
            return jsonify(status="false")
        elif check == int(checknum):
            User.register_first(g.db,email,passwrod,phonenum)
            return jsonify(status="success")
        else:
            return jsonify(status="false")

@allow_cross_domain
def register_second():
    if request.method == "POST":
        data = request.form
        phone = data["phonenum"]
        username = data["username"]
        university_id = data["universityid"]
        major_id = data["majorid"]
        gpa = data["gpa"]
        User.register_second(g.db,phone,username,university_id,major_id,gpa)
        return jsonify(status="success")
    return jsonify(status="false")

@allow_cross_domain
def logout():
    session.pop("username")
    return redirect("/index")



