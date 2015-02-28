
# -*- coding:utf-8 -*-
# Time: 14-2-22 下午11:48
# Desc: 短信http接口的python代码调用示例
import httplib
import urllib
from random import randint
import json
from flask import request, jsonify,g
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
        print request.data
       # print request.get_json()
        #print request.json
        data =  request.form
        #data = json.loads(data)
        print data
        print dir(data)
        print data.get("phonenum")
        print data.getlist
        cc = data.to_dict()
        print cc.keys()[0]
        print dir(cc.keys()[0])
        phone =  json.loads(cc.keys()[0])["phonenum"]
       # print data.fromkeys
        #print data.setlist()
        #print data.itervalues()
        #print dir(request)
        #phone = request.form[0]["phonenum"]
        #print phone
        #data = json.loads(request.data)
        #print data
        #phone = data["phone"]
        if len(phone) == 11:
            code = randint(1000, 9999)
            company = "游必有方"
            tpl_value = "#code#="+str(code)+"&#company#="+company
            result = tpl_send_sms(Config.apikey, 1, tpl_value, phone)
            code_num = json.loads(result)["code"]
            print code_num
            if code_num == 0:

                print User.set_sms_checknum(g.db, phone, code)
                return jsonify(status="success")
        return jsonify(status="false")