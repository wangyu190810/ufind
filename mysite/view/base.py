__author__ = 'wangyu'
from flask import session,wrappers,redirect
from functools import wraps
from flask import make_response


def validate_user_login(func):
    @wraps(func)
    def _validate_user_login(*args,**kwargs):
        if "username" in session:
            return func(*args,**kwargs)
        return redirect("/login")
    return _validate_user_login


def allow_cross_domain(fun):
    @wraps(fun)
    def wrapper_fun(*args, **kwargs):
        rst = make_response(fun(*args, **kwargs))
        rst.headers['Access-Control-Allow-Origin'] = '*'
        rst.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
        allow_headers = "Referer,Accept,Origin,User-Agent"
        rst.headers['Access-Control-Allow-Headers'] = allow_headers
        return rst
    return wrapper_fun




