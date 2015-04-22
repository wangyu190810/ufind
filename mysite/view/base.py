# -*-coding:utf-8-*-
__author__ = 'wangyu'
from flask import session
from functools import wraps
from flask import make_response, jsonify, g,request, current_app


import time
import urllib
import httplib
import json
from random import randint
from itsdangerous import Signer
import hashlib
import binascii
from mysite.model.user import User
from config import Config

def validate_user_login(func):
    @wraps(func)
    def _validate_user_login(*args, **kwargs):
        if "user_id" in session:
            return func(*args, **kwargs)
        return jsonify(status="no_login")
    return _validate_user_login


def jsonp(func):
    """Wraps JSONified output for JSONP requests."""
    @wraps(func)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            data = str(func(*args, **kwargs).data)
            content = str(callback) + '(' + data + ')'
            mimetype = 'application/javascript'
            return current_app.response_class(content, mimetype=mimetype)
        else:
            return func(*args, **kwargs)
    return decorated_function


def jsoncallback(jsonp_content,callback):
    return callback+"("+str(jsonp_content)+");"


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

def tpl_send_sms(apikey, tpl_id, tpl_value, mobile):
    """
    模板接口发短信
    """
    params = urllib.urlencode({'apikey': apikey, 'tpl_id':tpl_id,
                               'tpl_value': tpl_value, 'mobile':mobile})
    headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/plain"}
    conn = httplib.HTTPConnection(Config.yunpian.get("host"),
                                  port=Config.yunpian.get("post"), timeout=30)
    conn.request("POST", Config. yunpian.get("sms_tpl_send_uri"), params, headers)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    return response_str


def sms_check(phone):
    u"""手机验证是否符合规范"""
    if len(phone) == 11 and phone[:2] in ["13", "15", "17", "18"]:
        code = randint(1000, 9999)
        company = "游必有方"
        tpl_value = "#code#="+str(code)+"&#company#="+company
        result = tpl_send_sms(Config.apikey, 1, tpl_value, phone)
        code_num = json.loads(result)["code"]
        if code_num == 0:
            return code
    return False


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


def set_university_offer_wechat(universityname,user_type,num):
    if user_type == 0:
        wechat_type = "_Bachelor"
    else:
        wechat_type = "_Master_PHD"
    return u"http://www.ufindoffer.com/images/unimg/twodim/"+universityname+wechat_type+str(num)+".jpg"


def get_main_major(num,name):
    return u"http://www.ufindoffer.com/images/unimg/major/"+name+str(num)+".png"


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


def get_SAT(CR,M,W):
    return CR + M + W


def get_compare_score(GPA_TO,GPA_from,GPA):
    #if GPA_TO > GPA and GPA_from < GPA:

    if GPA is None:
        return True
    if float(GPA_from) <= float(GPA) and float(GPA_TO) >= float(GPA):
        return True
    elif float(GPA_from) >= float(GPA) and float(GPA_TO) <= float(GPA):
        return True
    return False


def set_password_salt(password):
    m = hashlib.sha224(password+Config.salt).hexdigest()
    return m


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
