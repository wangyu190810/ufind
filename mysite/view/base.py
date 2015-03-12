__author__ = 'wangyu'
from flask import session
from functools import wraps
from flask import make_response, jsonify, g

import time
from random import randint
from itsdangerous import Signer

from mysite.model.user import User
from config import Config


def validate_user_login(func):
    @wraps(func)
    def _validate_user_login(*args, **kwargs):
        if "user_id" in session:
            return func(*args, **kwargs)
        return jsonify(status="no_login")
    return _validate_user_login


def login_user_info(func):
    @wraps(func)
    def _login_user_info(*args, **kwargs):
        if "user_id" in session:
            user = User.get_user_info(g.db,session["user_id"])
            student = dict()
            student["studentid"] = user.id
            student["studentname"] = user.username
            student["studentpic"] = user.pic
            return jsonify(status="success",
                           student=student)
        return func(*args, **kwargs)
    return _login_user_info


def allow_cross_domain(fun):
    @wraps(fun)
    def wrapper_fun(*args, **kwargs):
        rst = make_response(fun(*args, **kwargs))
        rst.headers['Access-Control-Allow-Origin'] = '*'
        rst.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
        allow_headers = "Referer,Accept,Origin,User-Agent"
        rst.headers['Access-Control-Allow-Headers'] = allow_headers
        rst.headers["Access-Control-Allow-Credentials"] = True

        return rst
    return wrapper_fun


def get_university_img(universityname, num,shape):
    return "http://www.ufindoffer.com/images/unimg/all_un/"+str(universityname)+"/"+shape+"/"+str(num)+".jpg"


def get_university_logo(universityname):
    return "http://www.ufindoffer.com/images/unimg/all_logo/"+str(universityname)+".png"


def get_university_state(statename):
    return "http://www.ufindoffer.com/images/unimg/state/"+str(statename)+".jpg"


def get_user_hred_img(sex,max_num):
    return "http://www.ufindoffer.com/images/unimg/head/"+sex+"/"+str(randint(1,max_num))+".jpg"


def get_timestamp(create_time):
    timeArray = time.localtime(create_time)
    return time.strftime("%Y-%m-%d %H:%M:%S", timeArray)


def set_sign_safe(sign_file):
    s = Signer(Config.login_sign)
    return s.sign(sign_file)


def get_sign_safe(true_file):
    s= Signer(Config.login_sign)
    return s.unsign(true_file)