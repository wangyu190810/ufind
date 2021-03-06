# coding: utf-8
# email: khahux@163.com

from time import time

from flask import g, session, request, jsonify

from lib.decorators import allow_cross_domain, set_sign_safe,\
    checknum_timeout,set_password_salt
from models.user import User
from models.university_china import UniversityChina, SeniorHighSchool, \
    MajorChina
from models.offer import Offer
from time import time
from random import randint


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

    password = set_password_salt(data["password"])
    user = User.login_user(g.db, email=login_email,
                           phone=login_phone, password=password)

    if user is not None:
        session["user_id"] = user.id

        student = dict()
        student["studentid"] = user.id
        student["studentname"] = user.username
        student["studentpic"] = user.pic
        student["type"] = str(user.type)
        return jsonify(
            student=student,
            status="success",
            cookie=str(user.id))
    elif User.get_user_exist(g.db,email=login_email,phone=login_phone):
        return jsonify(status="password_error")
    return jsonify(status="user_not_exist")


@allow_cross_domain
def login_from_cookie():
    print request.method
    print request.form
    if request.method == "GET":

        user_id = session.get("user_id")
        user = User.get_user_info(g.db, user_id)
        if user is not None:
            session["user_id"] = user.id
            student = dict()
            student["studentid"] = user.id
            student["studentname"] = user.username
            student["studentpic"] = user.pic
            student["type"] = str(user.type)
            return jsonify(
                student=student,
                status="success",
            )
    return jsonify(status="false")


@allow_cross_domain
def register_first():
    if request.method == "POST":
        data = request.form
        phonenum = data["phonenum"]
        checknum = data["checknum"]

        check = User.get_checknum(g.db, phonenum)
        print request.form
        if check is None:
            return jsonify(status="false")
        elif check.checknum == int(checknum):
            print checknum_timeout(check.checknum_time)
            if checknum_timeout(check.checknum_time):
                return jsonify(status="success")
            return jsonify(status="checknum_timeout")

        else:
            return jsonify(status="checknum_error")


@allow_cross_domain
def register_second():
    if request.method == "POST":
        data = request.form

        email = data["email"]
        password = set_password_salt(data["password"])
        phone = data.get("phonenum")
        username = data.get("username")
        university_id = data.get("universityid")
        gpa = data["gpa"]
        user_type = data.get("type")
        if int(user_type) == 0:
            senior_dict = {
                '1': u"文科",
                '2': u"理科",
                '3': u"其他"
            }
            senior = SeniorHighSchool.get_senior_high(g.db, university_id)
            university_name = senior.name

            major_name = senior_dict.get(data.get("majorid"))
        else:
            university = UniversityChina.get_university_china_info(g.db, university_id)
            university_name = university.name
            major_id = int(data.get("majorid"))

            major_name = MajorChina.get_major_china(g.db, major_id).major_name

        create_time = time()
        active = 1
        if User.get_mobile_user_phone(g.db,phone):
            active = 2
        User.register_second(g.db, email,password,phone,
                             username, university_name, major_name,
                             gpa, user_type, create_time,active)
        user = User.get_user_info_by_phone(g.db, phone)
        user_id = user.id
        session["user_id"] = user_id
        incomplete = "false"
        if user.mobile_user == 2:
            incomplete = "true"
        User.update_user_pic(g.db,user_id,
                             """http://www.ufindoffer.com/images/unimg/head/%E6%97%A0%E6%80%A7%E5%88%AB/"""+
                             str(randint(1,17))+""".jpg""")
        Offer.update_offer_status(g.db,user_id)

        return jsonify(status="success",
                       cookie=str(user_id),
                       incomplete=incomplete)
    return jsonify(status="false")


@allow_cross_domain
def change_password():
    if request.method == "POST":
        data = request.form

        phone = data["phonenum"]
        password = set_password_salt(data["password"])
        checknum = data["checknum"]

        check = User.get_checknum(g.db, phone)
        if check.checknum == int(checknum) and checknum_timeout(check.checknum_time):
            User.change_password(g.db, phone, password)
            return jsonify(status="success")
        return jsonify(status="false")


@allow_cross_domain
def check_mobile_user_phone():
    if request.method == "POST":
        data = request.form
        phone = data.get("phonenum")
        if User.get_mobile_user_phone(g.db,phone):
            return jsonify(status="success")
    return jsonify(status="false")


@allow_cross_domain
def logout():
    session.pop("user_id")
    return jsonify(status="success")
