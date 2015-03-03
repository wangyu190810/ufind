# -*-coding:utf8-*-
__author__ = 'wangyu'
from flask import redirect, g, session, request, jsonify,make_response


from mysite.view.base import allow_cross_domain
from mysite.model.user import User

import time

@allow_cross_domain
def login():
    data = request.form
    print request.headers
    login_auth = data["email"]
    if "@" in login_auth:
        login_email = login_auth
        login_phone = None
    else:
        login_email = None
        login_phone = login_auth

    password = data["password"]
    user = User.login_user(g.db, email=login_email,
                           phone=login_phone, password=password)
    if user is not None:
        session["user_id"] = user.id
        resp = make_response()
        stuedent = dict()
        stuedent["studentid"] = user.id
        stuedent["studentname"] = user.username
        stuedent["studentpic"] = user.pic
        resp.set_cookie(key="user_id",value=str(user.id),domain="www.ufind.top",expires=time.time()+60*60)
        return jsonify(
            student = stuedent,
            status="success")
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
        if check_num == int(checknum):
            User.change_password(g.db, phone, password)
            return jsonify(status="success")
        return jsonify(status="false")


@allow_cross_domain
def logout():
    session.pop("username")
  #  user_id = request.cookies.get("user_id")

    return jsonify(status="success")



