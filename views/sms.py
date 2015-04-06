# coding: utf-8
# email: khahux@163.com

import json
import httplib
import urllib
from random import randint

from flask import request, jsonify, g

from models.user import User
from config import yunpian_config as y
from lib.decorators import allow_cross_domain


u"""查账户信息的URI"""
user_get_uri = "/" + y['version'] + "/user/get.json"
u"""通用短信接口的URI"""
sms_send_uri = "/" + y['version'] + "/sms/send.json"
u"""模板短信接口的URI"""
sms_tpl_send_uri = "/" + y['version'] + "/sms/tpl_send.json"

company = u"游必有方"


def generate_code():
    return randint(1000, 9999)


def tpl_send_sms(tpl_id, tpl_value, mobile):
    u"""模板接口发短信"""
    params = urllib.urlencode({
        'apikey': y['api_key'],
        'tpl_id': tpl_id,
        'tpl_value': tpl_value,
        'mobile': mobile})
    headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/plain"}
    conn = httplib.HTTPConnection(y['host'], port=y['port'], timeout=30)
    conn.request("POST", sms_tpl_send_uri, params, headers)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()

    return response_str


@allow_cross_domain
def send_sms():
    if request.method == "POST":
        data = request.form

        cc = data.to_dict()
        phonenum = eval(cc.keys()[0])
        phone = phonenum["phonenum"]
        sms_type = phonenum.get("type")
        user = User.get_user_info_by_phone(g.db, phone)
        if (user is None and sms_type == 0) or (user is not None and sms_type is None):
            if len(phone) == 11 and phone[:2] in ["13", "15", "17", "18"]:
                code = generate_code()
                tpl_value = "#code#="+str(code)+"&#company#="+company
                result = tpl_send_sms(1, tpl_value, phone)
                code_num = json.loads(result)["code"]
                if code_num == 0:

                    User.set_sms_checknum(g.db, phone, code)
                    return jsonify(status="success")
            return jsonify(status="false")
        elif user.username is None and sms_type == 0:
            code = generate_code()
            tpl_value = "#code#="+str(code)+"&#company#="+company
            result = tpl_send_sms(1, tpl_value, phone)
            code_num = json.loads(result)["code"]
            if code_num == 0:
                User.set_sms_checknum(g.db, phone, code)
                return jsonify(status="success")
            return jsonify(status="false")
        elif user.username is not None:
            return jsonify(status="registered")

    return jsonify(status="false")



