
# -*- coding:utf-8 -*-
# Time: 14-2-22 下午11:48
# Desc: 短信http接口的python代码调用示例
import httplib
import urllib
from random import randint
import json
from flask import request, jsonify,g,session
from config import Config

from mysite.model.user import User
from mysite.view.base import allow_cross_domain
# 服务地址
host = "yunpian.com"
# 端口号
port = 80
# 版本号
version = "v1"
# 查账户信息的URI
user_get_uri = "/" + version + "/user/get.json"
# 通用短信接口的URI
sms_send_uri = "/" + version + "/sms/send.json"
# 模板短信接口的URI
sms_tpl_send_uri = "/" + version + "/sms/tpl_send.json"


def tpl_send_sms(apikey, tpl_id, tpl_value, mobile):
    """
    模板接口发短信
    """
    params = urllib.urlencode({'apikey': apikey, 'tpl_id':tpl_id,
                               'tpl_value': tpl_value, 'mobile':mobile})
    headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/plain"}
    conn = httplib.HTTPConnection(host, port=port, timeout=30)
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
        user_change = User.get_user_info(g.db,session.get("user_id"))
        phonenum = eval(cc.keys()[0])
        phone = phonenum["phonenum"]
        sms_type = phonenum.get("type")
        user = User.get_user_info_by_phone(g.db,phone)
        print user,sms_type,phone
        # 注册发送验证码
        if (user is None and sms_type == 0) or (user is not None and sms_type is None):
            if len(phone) == 11 and phone[:2] in ["13", "15", "17", "18"]:
                code = randint(1000, 9999)
                company = "游必有方"
                tpl_value = "#code#="+str(code)+"&#company#="+company
                result = tpl_send_sms(Config.apikey, 1, tpl_value, phone)
                code_num = json.loads(result)["code"]
                if code_num == 0:

                    User.set_sms_checknum(g.db, phone, code)
                    return jsonify(status="success")
            return jsonify(status="false")
        if user is None and sms_type is None:
            return jsonify(status="phone_not_exist")

        # 找回密码

        elif user.username is None and sms_type == 0:
            if len(phone) == 11 and phone[:2] in ["13", "15", "17", "18"]:
                code = randint(1000, 9999)
                company = "游必有方"
                tpl_value = "#code#="+str(code)+"&#company#="+company
                result = tpl_send_sms(Config.apikey, 1, tpl_value, phone)
                code_num = json.loads(result)["code"]
                if code_num == 0:
                    User.set_sms_checknum(g.db, phone, code)
                    return jsonify(status="success")
            return jsonify(status="false")

        elif user_change is not None and sms_type == 1:
            if user is not None:
                return jsonify(status="registered")
            if len(phone) == 11 and phone[:2] in ["13", "15", "17", "18"]:
                code = randint(1000, 9999)
                company = "游必有方"
                tpl_value = "#code#="+str(code)+"&#company#="+company
                result = tpl_send_sms(Config.apikey, 1, tpl_value, phone)
                code_num = json.loads(result)["code"]
                if code_num == 0:
                    User.update_user_phone_old(g.db,user_id=user.id,phone=phone,checknum=code)
                    return jsonify(status="success")
            return jsonify(status="false")
        elif user.username is not None:
            return jsonify(status="registered")

    return jsonify(status="false")
