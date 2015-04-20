
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
from mysite.view.base import allow_cross_domain,sms_check,tpl_send_sms,set_university_offer_wechat
from mysite.model.offer import Offer
from mysite.model.major import Major
from mysite.model.university import University
from mysite.mobile.model import Prize


@allow_cross_domain
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
            return jsonify(status="user_exit")
        print user,sms_type,phone
        # 注册发送验证码
        if (user is None and sms_type == str(1)) or (user is not None and sms_type is None):
            code = sms_check(phone)
            if code:
                User.set_sms_checknum(g.db, phone, code)
                return jsonify(status="success")
        return jsonify(status="false")


@allow_cross_domain
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
                return jsonify(status="check_num_error")
        else:
            return jsonify(status="please_send_sms")

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
        return jsonify(status="success",
                       offerlist=offer_list,
                       description=User.get_user_info(g.db,user.id).description)


@allow_cross_domain
def get_user_prize():
    if request.method == "POST":
        phone = request.form.get("phone")
        user = User.get_user_info_by_phone(g.db,phone)
        if user:
            if user.coupon is not None:
                return jsonify(status="user_have_coupon")
        prize = Prize.get_random_prize(g.db)
        Prize.set_prize_user(g.db,prize.id,User.id)
        User.set_user_account(g.db,phone,prize.coupon,prize.account)
        return jsonify(status="success",
                       count=prize.account
                       )
    return jsonify(status="false")


@allow_cross_domain
def get_user_share():
    if request.method == "POST":
        phone = request.form.get("phone")
        pass
