
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
from mysite.view.base import allow_cross_domain,tpl_send_sms,sms_check


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
            code = sms_check(phone)
            if code:
                User.set_sms_checknum(g.db, phone, code)
                return jsonify(status="success")
            return jsonify(status="false")

        # 找回密码
        if user is None and sms_type is None:
            return jsonify(status="phone_not_exist")

        elif user.mobile_user == 2 and sms_type is None and user.user_name is None:
            return jsonify(status="phone_not_exist")

        elif sms_type == 0 and user.username is None :
            code = sms_check(phone)
            if code:
                User.set_sms_checknum(g.db, phone, code)
                return jsonify(status="success")
            return jsonify(status="false")

        elif user_change is not None and sms_type == 1:
            if user is not None:
                return jsonify(status="registered")
            code = sms_check(phone)
            if code:
                    User.update_user_phone_old(g.db,user_id=user.id,phone=phone,checknum=code)
                    return jsonify(status="success")
            return jsonify(status="false")
        elif user.username is not None:
            return jsonify(status="registered")

    return jsonify(status="false")
