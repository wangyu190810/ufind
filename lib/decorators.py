# coding: utf-8
# email: khahux@163.com

from functools import wraps

from flask import session, make_response, jsonify, g

from models.user import User


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
            user = User.get_user_info(g.db, session["user_id"])
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