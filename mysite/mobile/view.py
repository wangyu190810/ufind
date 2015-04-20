
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
from mysite.view.base import allow_cross_domain,sms_check,tpl_send_sms



@allow_cross_domain
def mobile_send_sms():
    if request.method == "POST":
        data = request.form
        cc = data.to_dict()
        phonenum = eval(cc.keys()[0])
        phone = phonenum["phonenum"]
        sms_type = phonenum.get("type")
        user = User.get_user_info_by_phone(g.db,phone)
        print user,sms_type,phone
        # 注册发送验证码
        if (user is None and sms_type == 0) or (user is not None and sms_type is None):
            code = sms_check(phone)
            if code:
                User.set_sms_checknum(g.db, phone, code)
                return jsonify(status="success")
        return jsonify(status="false")


def mobile_send_sms():

