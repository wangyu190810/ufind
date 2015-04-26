
# -*- coding:utf-8 -*-


import json
import time
from datetime import timedelta,datetime
import calendar

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


@allow_cross_domain
def mobile_send_sms():
    if request.method == "POST":
        data = request.form
        phone = data.get("phone")
        sms_type = data.get("type")

        user = User.get_user_info_by_phone(g.db,phone)
        print user,sms_type,phone
        if User.get_mobile_user_exit_by_phone(g.db,phone):
            return json.dumps({"status":"user_exit"})
        if User.get_mobile_user_prize_exit(g.db,phone):
            return json.dumps({"status": "get_prize"})
        # 注册发送验证码
        code = None
        if user is None and sms_type == str(1):
            code = sms_check(phone)
        elif user.grade is None and sms_type == str(1):
            code = sms_check(phone)

        if code:
            User.set_mobile_sms(g.db, phone, code)
            return json.dumps({"status": "success"})
        return json.dumps({"status": "false"})


@allow_cross_domain
def mobile_set_offer():
    if request.method == "POST":
        data = request.form
        university_id = data.get("university_id",int)
        offer_major_id = data.get("major_id",int)
        offer_major_name = data.get("major_name")
        user_type = data.get("user_type",int)

        grade = data.get("grade")
        phone = data.get("phone")
        check_num = data.get("check_num")

        user_check = User.get_checknum(g.db,phone)
        if user_check is None:
            return json.dumps({"status": "user_not_exit"})
        print user_check
        print data,check_num
        if check_num == "":
            print("adfasdf")
        else:
            type(check_num),

        if check_num != "":
            if str(user_check.checknum) == check_num:
                User.set_mobile_user_grade(g.db,phone,grade)
                user = User.get_user_info_by_phone(g.db,phone)
            else:
                return json.dumps({"status":"check_num_error"})


        id_major = None
        offer_status = 1
        if offer_major_id is None:
            print offer_major_id,"123123"
        if offer_major_id == "":
            print "fasdfasd"
        if offer_major_name and offer_major_id is None:

            major_key = Major.get_major_exit(g.db,offer_major_name)
            print major_key
            school1_id = 7
            main_major = "NotMatched"
            major_user_type =2
            offer_status = 2
            if major_key:
                major_info = Major.get_major_info_by_mame(g.db,offer_major_name)
                if major_info:
                    school1_id = major_info.faculty_id
                    major_user_type = 1
                    main_major = major_info.main_major
                    offer_status = 1
            id_major = Major.add_major(g.db,name=offer_major_name,
                                        main_major=main_major,
                                        university_id=university_id,
                                        major_type=user.type,
                                        faculty_id=school1_id,
                                        major_user_type=major_user_type
                                )

        if id_major:
            major_id_info = Major.get_major_info_by_id_scalar(g.db,id_major)
            offer_major_id = id_major
        else:
            major_id_info = Major.get_major_info_by_id_scalar(g.db,offer_major_id)



        school1_id = 0
        school2_id = 0
        school3_id = 0
        if major_id_info:
            school1_id = major_id_info.faculty_id
            school2_id = major_id_info.School2_ID
            school3_id = major_id_info.School3_ID
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
        print offer_major_id
        Offer.del_same_offer(g.db,university_id=university_id,
                                major_id =offer_major_id,user_id=user_check.id)


        Offer.set_offer_mobile(g.db,user_id=user_check.id,
                               university_id=university_id,
                               major_id=offer_major_id,
                               school1_id=school1_id,
                               school2_id=school2_id,
                               school3_id=school3_id,
                               user_type=user_type,
                               grade=grade,
                               wechat=wechat,
                               offer_type="AD",
                               offer_status=offer_status
                               )
        offer_list = list()
        checkList = list()
        university_name = None
        twodim = None
        for last_offer in Offer.get_mobile_user_last_offer(g.db,user_check.id):
            print last_offer
            try:
                university_name = University.get_university_from_id(g.db,last_offer[1])
                twodim = last_offer[2]
            except IndexError:
                university_name = None

        offer_dict = dict()
        if university_name:
            offer_dict["universityname"] = university_name.chiname
            offer_dict["logo"] = get_university_logo(university_name.name)
            offer_dict["twodim"] = twodim

            offer_list.append(offer_dict)

        return json.dumps({"status":"success",
                       "offerlist":offer_list,
                       "description":User.get_user_info(g.db,user_check.id).description})

@allow_cross_domain
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
        return json.dumps({"status":"success",
                       "user_info":user_info})
    return json.dumps({"status":"false"})


@allow_cross_domain
def get_user_prize():
    if request.method == "POST":
        phone = request.form.get("phone")
        user = User.get_user_info_by_phone(g.db,phone)
        if user:
            if user.account is not None:
                return json.dumps({"status":"user_have_coupon"})
        prize = Prize.get_random_prize(g.db)
        if prize is None:
            not_coupon = Prize.get_random_prize_not_coupon(g.db)
            User.set_user_account(g.db, phone, None, not_coupon.account)
            return json.dumps({"status": "success",
                                "acount": not_coupon.account})
        Prize.set_prize_user(g.db,prize.id,user.id)
        User.set_user_account(g.db,phone,prize.coupon,prize.account)
        return json.dumps({"status":"success",
                       "acount":prize.account
                       })
    return json.dumps({"status":"false"})


@allow_cross_domain
def get_user_share():
    if request.method == "POST":
        phone = request.form.get("phone")
        share_type = request.form.get("share")
        user = User.get_user_info_by_phone(g.db,phone)
        if user:
            if Prize.get_share_prize(g.db,user.id):
                prize_user = Prize.get_user_prize(g.db,user_id=user.id)
                User.set_user_account(g.db,phone,prize_user.coupon,prize_user.account)

                return json.dumps({"status":"success"})
    return json.dumps({"status":"false"})

@allow_cross_domain
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
            return json.dumps(university_jsonp)
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
            return json.dumps(university_jsonp)


@allow_cross_domain
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
        searchname,university_id,grade = map(request.args.get,
                                       ("searchname", "universityid","grade"))

        print request.args
        if university_id is None:
            for row in Major.search_maior(g.db, searchname):
                major["name"] = row.name
                major["chiname"] = row.chiname
                major["id"] = row.id
                major_list.append(major)
                major = {}
            major_json = {"namelist":major_list}
            major_json["status"] = "success"
            return json.dumps(major_json)
        else:
            if searchname is None:
                searchname = ""
            for row in Major.search_maior(g.db, searchname, university_id,grade):
                major["name"] = row.name
                major["chiname"] = row.chiname
                major["id"] = row.id
                major_list.append(major)
                major = {}
            major_json = {"namelist":major_list}
            major_json["status"] = "success"
            return json.dumps(major_json)


def get_mobile_prize_deadline():
    u"""活动截止时间"""
    #last_now = datetime.now()+ timedelta(7)
    #last_ts = calendar.timegm(last_now.utctimetuple())
    now = datetime.utcnow()
    last = 1431273600 - calendar.timegm(now.utctimetuple())
    return json.dumps({"deadline": last})


def get_random_prize_test():
    return json.dumps(Prize.get_random_prize(g.db).account)

