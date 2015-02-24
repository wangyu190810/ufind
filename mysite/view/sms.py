# -*-coding:utf-8-*-
__author__ = 'wangyu'
#
import base64
import datetime
import urllib2
import md5

import json
from flask import request,g
from mysite.view.base import allow_cross_domain
from mysite.model.state import State

# 返回签名
def getSig(accountSid,accountToken,timestamp):
    sig = accountSid + accountToken + timestamp
    return md5.new(sig).hexdigest().upper()

#生成授权信息
def getAuth(accountSid,timestamp):
    src = accountSid + ":" + timestamp
    return base64.encodestring(src).strip()

#发起http请求
def urlOpen(req,data=None):
    try:
        res = urllib2.urlopen(req,data)
        data = res.read()
        res.close()
    except urllib2.HTTPError, error:
        data = error.read()
        error.close()
    return data

#生成HTTP报文
def createHttpReq(req,url,accountSid,timestamp,responseMode,body):
    req.add_header("Authorization", getAuth(accountSid,timestamp))
    if responseMode:
        req.add_header("Accept","application/"+responseMode)
        req.add_header("Content-Type","application/"+responseMode+";charset=utf-8")
    if body:
        req.add_header("Content-Length",len(body))
        req.add_data(body)
    return req
#
import base64
import datetime
import urllib2
import md5

# 返回签名
def getSig(accountSid,accountToken,timestamp):
    sig = accountSid + accountToken + timestamp
    return md5.new(sig).hexdigest().upper()

#生成授权信息
def getAuth(accountSid,timestamp):
    src = accountSid + ":" + timestamp
    return base64.encodestring(src).strip()

#发起http请求
def urlOpen(req,data=None):
    try:
        res = urllib2.urlopen(req,data)
        data = res.read()
        res.close()
    except urllib2.HTTPError, error:
        data = error.read()
        error.close()
    return data

#生成HTTP报文
def createHttpReq(req,url,accountSid,timestamp,responseMode,body):
    req.add_header("Authorization", getAuth(accountSid,timestamp))
    if responseMode:
        req.add_header("Accept","application/"+responseMode)
        req.add_header("Content-Type","application/"+responseMode+";charset=utf-8")
    if body:
        req.add_header("Content-Length",len(body))
        req.add_data(body)
    return req
#
import base64
import datetime
import urllib2
import md5

# 返回签名
def getSig(accountSid,accountToken,timestamp):
    sig = accountSid + accountToken + timestamp
    return md5.new(sig).hexdigest().upper()

#生成授权信息
def getAuth(accountSid,timestamp):
    src = accountSid + ":" + timestamp
    return base64.encodestring(src).strip()

#发起http请求
def urlOpen(req,data=None):
    try:
        res = urllib2.urlopen(req,data)
        data = res.read()
        res.close()
    except urllib2.HTTPError, error:
        data = error.read()
        error.close()
    return data

#生成HTTP报文
def createHttpReq(req,url,accountSid,timestamp,responseMode,body):
    req.add_header("Authorization", getAuth(accountSid,timestamp))
    if responseMode:
        req.add_header("Accept","application/"+responseMode)
        req.add_header("Content-Type","application/"+responseMode+";charset=utf-8")
    if body:
        req.add_header("Content-Length",len(body))
        req.add_data(body)
    return req
#
import base64
import datetime
import urllib2
import md5

# 返回签名
def getSig(accountSid,accountToken,timestamp):
    sig = accountSid + accountToken + timestamp
    return md5.new(sig).hexdigest().upper()

#生成授权信息
def getAuth(accountSid,timestamp):
    src = accountSid + ":" + timestamp
    return base64.encodestring(src).strip()

#发起http请求
def urlOpen(req,data=None):
    try:
        res = urllib2.urlopen(req,data)
        data = res.read()
        res.close()
    except urllib2.HTTPError, error:
        data = error.read()
        error.close()
    return data

#生成HTTP报文
def createHttpReq(req,url,accountSid,timestamp,responseMode,body):
    req.add_header("Authorization", getAuth(accountSid,timestamp))
    if responseMode:
        req.add_header("Accept","application/"+responseMode)
        req.add_header("Content-Type","application/"+responseMode+";charset=utf-8")
    if body:
        req.add_header("Content-Length",len(body))
        req.add_data(body)
    return req
#
import base64
import datetime
import urllib2
import md5

# 返回签名
def getSig(accountSid,accountToken,timestamp):
    sig = accountSid + accountToken + timestamp
    return md5.new(sig).hexdigest().upper()

#生成授权信息
def getAuth(accountSid,timestamp):
    src = accountSid + ":" + timestamp
    return base64.encodestring(src).strip()

#发起http请求
def urlOpen(req,data=None):
    try:
        res = urllib2.urlopen(req,data)
        data = res.read()
        res.close()
    except urllib2.HTTPError, error:
        data = error.read()
        error.close()
    return data

#生成HTTP报文
def createHttpReq(req,url,accountSid,timestamp,responseMode,body):
    req.add_header("Authorization", getAuth(accountSid,timestamp))
    if responseMode:
        req.add_header("Accept","application/"+responseMode)
        req.add_header("Content-Type","application/"+responseMode+";charset=utf-8")
    if body:
        req.add_header("Content-Length",len(body))
        req.add_data(body)
    return req


# displayNum 被叫显示的号码
# templateId 模板Id
class RestAPI:

    HOST = "https://api.ucpaas.com"
    PORT = ""
    SOFTVER = "2014-06-30"
    JSON = "json"
    XML = "xml"

    #主账号信息查询
    #accountSid  主账号ID
    #accountToken 主账号的Token
    def getAccountInfo(self,accountSid,accountToken,isUseJson=True):
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")
        signature = getSig(accountSid,accountToken,timestamp)
        url = self.HOST + ":" + self.PORT + "/" + self.SOFTVER + "/Accounts/" + accountSid + "?sig=" + signature

        if isUseJson == True:
            responseMode = self.JSON
        else:
            responseMode = self.XML

        req = urllib2.Request(url)
        return urlOpen(createHttpReq(req,url,accountSid,timestamp,responseMode,None))


    #申请client账号
    #accountSid  主账号ID
    #accountToken 主账号的Token
    #appId 应用ID
    #clientType 计费方式。0  开发者计费；1 云平台计费。默认为0.
    #charge 充值的金额
    #friendlyName 昵称
    #mobile 手机号码
    def applyClient(self,accountSid,accountToken,appId,clientType,charge,friendlyName,mobile,isUseJson=True):
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")
        signature = getSig(accountSid,accountToken,timestamp)
        url = self.HOST + ":" + self.PORT + "/" + self.SOFTVER + "/Accounts/" + accountSid + "/Clients?sig=" + signature

        if isUseJson == True:
            body = '{"client":{"appId":"%s","clientType":"%s","charge":"%s","friendlyName":"%s","mobile":"%s"}}'\
                %(appId,clientType,charge,friendlyName,mobile)
            responseMode = self.JSON
        else:
            body = '<?xml version="1.0" encoding="utf-8"?>\
                    <client>\
                        <appId>%s</appId>\
                        <clientType>%s</clientType>\
                        <charge>%s</charge>\
                        <friendlyName>%s</friendlyName>\
                        <mobile>%s</mobile>\
                    </client>\
                    '%(appId,clientType,charge,friendlyName,mobile)
            responseMode = self.XML

        req = urllib2.Request(url)
        return urlOpen(createHttpReq(req,url,accountSid,timestamp,responseMode,body))


    #释放client账号
    #accountSid  主账号ID
    #accountToken 主账号的Token
    #clientNumber 子账号
    #appId 应用ID
    def ReleaseClient(self,accountSid,accountToken,clientNumber,appId,isUseJson=True):
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")
        signature = getSig(accountSid,accountToken,timestamp)
        url = self.HOST + ":" + self.PORT + "/" + self.SOFTVER + "/Accounts/" + accountSid + "/dropClient?sig=" + signature

        if isUseJson == True:
            body = '{"client":{"clientNumber":"%s","appId":"%s"}}'%(clientNumber,appId)
            responseMode = self.JSON
        else:
            body = '<?xml version="1.0" encoding="utf-8"?>\
                    <client>\
                        <clientNumber>%s</clientNumber>\
                        <appId>%s</appId >\
                    </client>\
                    '%(clientNumber,appId)
            responseMode = self.XML

        req = urllib2.Request(url)
        return urlOpen(createHttpReq(req,url,accountSid,timestamp,responseMode,body))


    #短信验证码（模板短信）
    #accountSid 主账号ID
    #accountToken 主账号Token
    #appId 应用ID
    #toNumber 被叫的号码
    #templateId 模板Id
    #param <可选> 内容数据，用于替换模板中{数字}
    def templateSMS(self,accountSid,accountToken,appId,toNumbers,templateId,param,isUseJson=True):
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")
        signature = getSig(accountSid,accountToken,timestamp)
        url = self.HOST + ":" + self.PORT + "/" + self.SOFTVER + "/Accounts/" + accountSid + "/Messages/templateSMS?sig=" + signature

        if isUseJson == True:
            body = '{"templateSMS":{ "appId":"%s","to":"%s","templateId":"%s","param":"%s"}}'%(appId,toNumbers,templateId,param)
            responseMode = self.JSON
        else:
            body = "<?xml version='1.0' encoding='utf-8'?>\
                    <templateSMS>\
                        <appId>%s</appId>\
                        <to>%s</to>\
                        <templateId>%s</templateId>\
                        <param>%s</param>\
                    </templateSMS>\
                    "%(appId,toNumbers,templateId,param)
            responseMode = self.XML

        req = urllib2.Request(url)
        return urlOpen(createHttpReq(req,url,accountSid,timestamp,responseMode,body))

def main():
    test = RestAPI()

    accountSid = "2ed639e783c000458eb63d15df2396bf"
    accountToken = "87cbc667b06108d52df685913b042975"
    appId = "daec7c81e660437d947eb632c0dd911e"

    to="13012345678"
    fromClient="66098000367509"
    fromSerNum="075512345678"
    toSerNum="13512345678"
    clientNumber="66098000367509"

    mobile = "15012345678"
    friendlyName = "test007"
    # 1分钱 = 10000。 charge单位是元
    charge = "8"
    clientType = "1"

    start = "0"
    limit = "100"
    isUseJson = True
    date = "day"
    chargeType="0"
    maxAllowTime="60"



    displayNum="28025790615"
    verifyCode="121324"
    toNumber="13804416205"
    templateId="3492"
    param="3321"


    #查询主账号
    #print(test.getAccountInfo(accountSid,accountToken,isUseJson))
    #申请子账号
    #print(test.applyClient(accountSid,accountToken,appId,clientType,charge,friendlyName,mobile,isUseJson))
    #查询子账号列表
    #print(test.getClientList(accountSid,accountToken,appId,start,limit,isUseJson))
    #删除一个子账号
    #print(test.ReleaseClient(accountSid,accountToken,clientNumber,appId,isUseJson))
    #查询子账号信息(clientNumber方式)
    #print(test.getClientInfo(accountSid,accountToken,appId,clientNumber,isUseJson))
    #查询子账号信息(mobile方式)
    #print(test.getClientInfoByMobile(accountSid,accountToken,appId,mobile,isUseJson))
    #查询应用话单
    #print(test.getBillList(accountSid,accountToken,appId,date,isUseJson))
    #子账号充值
    #print(test.chargeClient(accountSid,accountToken,appId,clientNumber,chargeType,charge,isUseJson))
    #回拨
    #print(test.callBack(accountSid,accountToken,appId,fromClient,to,fromSerNum,toSerNum,maxAllowTime,isUseJson))
    #语音验证码
    #print(test.voiceCode(accountSid,accountToken,appId,verifyCode,toNumber,isUseJson))
    #短信
    a = test.templateSMS(accountSid,accountToken,appId,toNumber,templateId,param,isUseJson)
    return a

def send_sms():
    if request.method == "GET":
        data = main()

        return json.dumps(data)
