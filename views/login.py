# coding: utf-8
# email: khahux@163.com

from flask import g, session, request, jsonify

from ufindoffer.views.base import allow_cross_domain, set_sign_safe,\
    checknum_timeout
from ufindoffer.models.user import User
from ufindoffer.models.university_china import UniversityChina, SeniorHighSchool, \
    MajorChina

from time import time


@allow_cross_domain
def login():
    data = request.form
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
        student = dict()
        student["studentid"] = user.id
        student["studentname"] = user.username
        student["studentpic"] = user.pic
        return jsonify(
            student=student,
            status="success",
            cookie=set_sign_safe(str(user.id)))
    return jsonify(status="false")


@allow_cross_domain
def login_from_cookie():
    if request.method == "GET":
        user_id = session.get("user_id")
        user = User.get_user_info(g.db, user_id)
        if user is not None:
            session["user_id"] = user.id
            student = dict()
            student["studentid"] = user.id
            student["studentname"] = user.username
            student["studentpic"] = user.pic
            return jsonify(
                student=student,
                status="success")
    return jsonify(status="false")


@allow_cross_domain
def register_first():
    if request.method == "POST":
        data = request.form
        email = data["email"]
        password = data["password"]
        phonenum = data["phonenum"]
        checknum = data["checknum"]
        check = User.get_checknum(g.db, phonenum)
        if check is None:
            return jsonify(status="false")
        elif check.checknum == int(checknum):
            if checknum_timeout(check.checknum_time):
                User.register_first(g.db, email, password, phonenum)
                return jsonify(status="success")
            return jsonify(status="checknum_timeout")
        else:
            return jsonify(status="false")


@allow_cross_domain
def register_second():
    if request.method == "POST":
        data = request.form
        phone = data.get("phonenum")
        username = data.get("username")
        university_id = data.get("universityid")
        user_type = data.get("type")
        if int(user_type) == 0:
            senior = SeniorHighSchool.get_senior_high(g.db, university_id)
            university_name = senior.name
            senior_dict = dict()
            senior_dict["1"] = u"文科"
            senior_dict["2"] = u"理科"
            senior_dict["3"] = u"其他"
            major_name = senior_dict.get(data.get("majorid"))
        else:
            university = UniversityChina.get_university_china_info(g.db,
                                                                   university_id)
            university_name = university.name
            major_id = int(data.get("majorid"))
            major_name = MajorChina.get_major_china(g.db, major_id).major_name
        gpa = data["gpa"]
        create_time = time()
        User.register_second(g.db, phone, username, university_name, major_name,
                             gpa, user_type, create_time)
        user = User.get_user_info_by_phone(g.db, phone)
        user_id = user.id
        session["user_id"] = user_id
        User.update_user_pic(g.db, user_id,
                             """http://www.ufindoffer.com/images/unimg/head
                             /%E6%97%A0%E6%80%A7%E5%88%AB/9.jpg""")
        return jsonify(status="success",
                       cookie=set_sign_safe(str(user_id)))
    return jsonify(status="false")


@allow_cross_domain
def change_password():
    if request.method == "POST":
        data = request.form
        phone = data["phonenum"]
        password = data["password"]
        checknum = data["checknum"]
        check = User.get_checknum(g.db, phone)
        if check.checknum == int(checknum) and \
                checknum_timeout(check.checknum_time):
            User.change_password(g.db, phone, password)
            return jsonify(status="success")
        return jsonify(status="false")


@allow_cross_domain
def logout():
    session.pop("user_id")
    return jsonify(status="success")
