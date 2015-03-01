# -*-coding:utf8-*-
__author__ = 'wangyu'
from flask import redirect, g, session, request, jsonify
from mysite.view.base import allow_cross_domain
from mysite.model.user import User


@allow_cross_domain
def login():
    data = request.form
    email = data["email"]
    password = data["password"]
    user = User.login_user(g.db, email, password)
    if user is not None:
        student = dict()
        session["user_id"] = user.id
        student["studentid"] = user.id
        student["studentname"] = user.username
        student["studentpic"] = user.pic
        print student
        return jsonify(status="success",
                       student=student)
    return jsonify(status="false")


@allow_cross_domain
def register_first():
    if request.method == "POST":
        print request.data
        data = request.form
        print data
        email = data["email"]
        password = data["password"]
        phonenum = data["phonenum"]
        checknum = data["checknum"]
        check = User.get_checknum(g.db, phonenum)
        if check is None:
            return jsonify(status="false")
        elif check == int(checknum):
            User.register_first(g.db, email, password, phonenum)
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
        User.register_second(g.db, phone, username, university_id, major_id,
                             gpa)
        return jsonify(status="success")
    return jsonify(status="false")


@allow_cross_domain
def change_password():
    if request.method == "POST":
        data = request.form
        phone = data["phonenum"]
        password = data["password"]
        checknum = data["checknum"]
        print phone,password,checknum
        check_num = User.get_checknum(g.db, phone)
        print check_num
        if check_num == checknum:
            User.change_password(g.db, phone, password)
            return jsonify(status="success")
        return jsonify(status="false")


@allow_cross_domain
def logout():
    session.pop("username")
    return redirect("/index")



