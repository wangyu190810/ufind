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
    return u"http://www.ufindoffer.com/images/unimg/all_un/"+universityname+u"/"+shape+u"/"+unicode(num)+".jpg"


def get_university_logo(universityname):
    return u"http://www.ufindoffer.com/images/unimg/all_logo/"+universityname+".png"


def get_university_state(statename):
    return u"http://www.ufindoffer.com/images/unimg/state/"+statename+".jpg"


def get_user_hred_img(sex,max_num):
    return u"http://www.ufindoffer.com/images/unimg/head/"+unicode(sex)+"/"+unicode(max_num)+".jpg"


def get_university_twodim(universityname):
    return u"http://www.ufindoffer.com/images/unimg/twodim/"+universityname+".jpg"


def get_timestamp(create_time):
    timeArray = time.localtime(create_time)
    return time.strftime("%Y-%m-%d %H:%M:%S", timeArray)


def get_Total(r, l, s, w):
    return r+l+s+w


def get_TELTS(r, l, s, w):
    score = float(r+l+s+w)/4
    if int((score * 10) / 10) == score:
        return score
    elif (score * 10) % 5 == 0:
        return score
    elif (score * 10) % 5 < 5:
        return int(score)
    elif (score * 10) % 5 > 5:
        return int(score)+1


def get_gre(v, q):
    return v+q


def get_GMAT(v,q):
    return v + q


def get_STA(CR,M,W):
    return CR + M + W


def set_sign_safe(sign_file):
    s = Signer(Config.login_sign)
    return s.sign(sign_file)


def get_sign_safe(true_file):
    s= Signer(Config.login_sign)
    return s.unsign(true_file)


def checknum_timeout(sms_time):
    if ((time.time() - sms_time) / 60) > 30:
        return False
    return True
