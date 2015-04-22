
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
from mysite.view.base import allow_cross_domain,sms_check,\
    tpl_send_sms,set_university_offer_wechat,get_university_logo,jsonp,\
    jsoncallback
from mysite.model.offer import Offer
from mysite.model.major import Major
from mysite.model.university import University
from mysite.mobile.model import Prize


@jsonp
def mobile_send_sms():
    if request.method == "POST":
        data = request.form
        print data
        # cc = data.to_dict()
        # phonenum = eval(cc.keys()[0])
        # phone = phonenum["phonenum"]
        # sms_type = phonenum.get("type")
        phone = data.get("phone")
        sms_type = data.get("type")
        user = User.get_user_info_by_phone(g.db,phone)
        if user:
            return jsoncallback(jsonify(status="user_exit"))
        print user,sms_type,phone
        # 注册发送验证码
        if (user is None and sms_type == str(1)) or (user is not None and sms_type is None):
            code = sms_check(phone)
            if code:
                User.set_sms_checknum(g.db, phone, code)
                return jsoncallback(jsonify(status="success"))
        return jsoncallback(jsonify(status="false"))


@jsonp
def mobile_set_offer():
    if request.method == "POST":
        data = request.form
        university_id = data.get("university_id")
        major_id = data.get("major_id")
        user_type = data.get("user_type")
        grade = data.get("grade")
        phone = data.get("phone")
        check_num = data.get("check_num")

        user_check = User.get_checknum(g.db,phone)
        print data,user_check.checknum
        if user_check:
            if str(user_check.checknum) == check_num:
                User.set_mobile_user_grade(g.db,phone,grade)
                user = User.get_user_info_by_phone(g.db,phone)
            else:
                return jsoncallback(jsonify(status="check_num_error"))
        else:
            return jsoncallback(jsonify(status="please_send_sms"))

        major_id = Major.get_major_info_by_id_scalar(g.db,major_id)
        school1_id = 0
        school2_id = 0
        school3_id = 0
        if major_id:
            school1_id = major_id.faculty_id
            school2_id = major_id.School2_ID
            school3_id = major_id.School3_ID
        offer_num = Offer.get_offer_num(g.db,university_id,user_type)
        num_wechat = 1
        if offer_num:
            if offer_num < 100:
                num_wechat = 1
            elif 100 <= offer_num < 200:
                num_wechat = 2
            elif 200 <= offer_num < 300:
                num_wechat = 3

        wechat=set_university_offer_wechat(University.get_university_from_id(g.db,university_id).short_name,user_type,num_wechat)
        Offer.set_offer_mobile(g.db,user_id=user.id,
                               university_id=university_id,
                               major_id=major_id,
                               school1_id=school1_id,
                               school2_id=school2_id,
                               school3_id=school3_id,
                               user_type=user_type,
                               grade=grade,
                               wechat=wechat
                               )
        offer_list = list()
        checkList = list()
        for row_user in Offer.get_offer_student_info(g.db,user.id):
            offer_dict = dict()
            offer_dict["universityid"] = row_user.university_id
            university_name = University.get_university_from_id(g.db,row_user.university_id)
            if university_name:
                offer_dict["universityname"] = university_name.chiname
                offer_dict["twodim"] = row_user.wechat
                if row_user.university_id not in checkList:
                    offer_list.append(offer_dict)
                    checkList.append(row_user.university_id)
        return jsoncallback(jsonify(status="success",
                       offerlist=offer_list,
                       description=User.get_user_info(g.db,user.id).description))

@jsonp
def get_mobile_user_info():
    u"""获取用户的信息"""
    if request.method == "GET":
        phone = request.form.get("phone")
        user = User.get_user_info_by_phone(g.db,phone)
        user_info = dict()
        if user:
            user_info["user_type"] = user.type
            user_info["grade"] = user.grade
            user_info["phone"] = user.phone
        return jsoncallback(jsonify(status="success",
                       user_info=user_info))
    return jsoncallback(jsonify(status="false"))


@jsonp
def get_user_prize():
    if request.method == "POST":
        phone = request.form.get("phone")
        user = User.get_user_info_by_phone(g.db,phone)
        if user:
            if user.coupon is not None:
                return jsoncallback(jsonify(status="user_have_coupon"))
        prize = Prize.get_random_prize(g.db)
        if prize is None:
            return jsoncallback(jsonify(status="success",
                       acount=None
                       ))
        Prize.set_prize_user(g.db,prize.id,user.id)
        User.set_user_account(g.db,phone,prize.coupon,prize.account)

        return jsoncallback(jsonify(status="success",
                       acount=prize.account
                       ))
    return jsoncallback(jsonify(status="false"))


@jsonp
def get_user_share():
    if request.method == "POST":
        phone = request.form.get("phone")
        share_type = request.form.get("share")
        user = User.get_user_info_by_phone(g.db,phone)
        if user:
            print "user"
            if Prize.get_share_prize(g.db,user.id):
                prize_user = Prize.get_user_prize(g.db,user_id=user.id)
                User.set_user_account(g.db,phone,prize_user.coupon,prize_user.account)

                return jsoncallback(jsonify(status="success"))
    return jsoncallback(jsonify(status="false"))

@jsonp
def get_mobile_search_university():
    if request.method == "GET":
        print request.data
        searchname, stateid,callback = map(request.args.get,("searchname","stateid","jsoncallback"))
        universitylist = []
        university = {}
        if stateid is None:

            for row in University.search_university(g.db,searchname):
                university["name"] = row.name
                university["chiname"] = row.chiname
                university["id"] = row.id
                university["logo"] = get_university_logo(row.name)
                universitylist.append(university)
                university = {}
            university_jsonp = {"namelist":universitylist}
            university["status"] = "success"
            return jsoncallback(json.dumps(university_jsonp),callback)
        else:
            for row in University.search_university(g.db,searchname,stateid):
                university["name"] = row.name
                university["chiname"] = row.chiname
                university["id"] = row.id
                university["logo"] = get_university_logo(row.name)
                universitylist.append(university)
                university = {}
            university_jsonp = {"namelist":universitylist}
            university["status"] = "success"
            return jsoncallback(json.dumps(university_jsonp),callback)


@jsonp
def get_mobile_search_major():
    """专业搜索"""
    if request.method == "GET":
        major_list = []
        major = {}
        user_id = session.get("user_id")
        user = User.get_user_info(g.db,user_id)
        major_type = None
        if user:
            major_type = user.type
        searchname,university_id,callback = map(request.args.get,
                                       ("searchname", "universityid","jsoncallback"))

        if university_id is None:
            for row in Major.search_maior(g.db, searchname):
                major["name"] = row.name
                major["chiname"] = row.chiname
                major["id"] = row.id
                major_list.append(major)
                major = {}
            return jsoncallback(jsonify(namelist=major_list,
                           status="success"),callback)
        else:
            for row in Major.search_maior(g.db, searchname, university_id,major_type):
                major["name"] = row.name
                major["chiname"] = row.chiname
                major["id"] = row.id
                major_list.append(major)
                major = {}
            return jsoncallback(jsonify(namelist=major_list,
                           status="success"),callback)