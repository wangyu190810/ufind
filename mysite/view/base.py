__author__ = 'wangyu'
from flask import session,wrappers,redirect
from functools import wraps
from flask import make_response,jsonify

import time

from mysite.model.user import User


def validate_user_login(func):
    @wraps(func)
    def _validate_user_login(*args,**kwargs):
        if "username" in session:
            return func(*args,**kwargs)
        return redirect("/login")
    return _validate_user_login


def login_user_info(func):
    @wraps(func)
    def _login_user_info(*args,**kwargs):
        if "user_id" in session:
            user = User.get_user_info()
            student = dict()
            student["studentid"] =user.id
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

def get_university_img(universityname,num):
    return "http://www.22too.com/US(150115)/intimer/"+str(universityname)+"/"+str(num)+".jpg"


def get_university_logo(universityname):
    return "http://www.22too.com/US LOGO/"+str(universityname)+".png"


def get_timestamp(create_time):
    timeArray = time.localtime(create_time)
    return time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

