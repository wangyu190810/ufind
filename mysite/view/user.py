# -*-coding:utf-8-*-
__author__ = 'wangyu'

from flask import g, jsonify, request, session
import json

from mysite.model.user import User, UserFollow
from mysite.view.base import allow_cross_domain, get_timestamp, \
    validate_user_login,get_university_logo,get_university_twodim,\
    get_GMAT, get_gre, get_TELTS, get_Total,get_SAT,get_compare_score,\
    checknum_timeout,set_password_salt
from mysite.model.offer import Offer
from mysite.model.university import University
from mysite.model.major import Major
from mysite.model.compare import CompareInfo, Compare
from mysite.model.message import Message
from mysite.model.score import Score
from mysite.model.stasub import Stasub

@validate_user_login
@allow_cross_domain
def get_user_info():
    if request.method == "GET":
        student_id = request.args.get("studentid")
        student_info = {}
        row = User.get_user_info(g.db, student_id)
        if row is None:
            return jsonify(status="false")

        student_info["prevuniversity"] = row.prevuniversity
        student_info["name"] = row.username
        student_info["prevmajor"] = row.prevmajor
        student_info["GPA"] = row.GPA
        student_info["TOEFL"] = row.TOEFL
        student_info["IELTS"] = row.IELTS
        student_info["GMAT"] = row.GMAT
        student_info["SAT"] = row.SAT
        student_info["GRE"] = row.GRE

        student_info["pic"] = row.pic
        student_info["grade"] = row.grade
        universityname = list()
        for row in Offer.get_offer_student_info(g.db, student_id):
            universityname.append(
                University.get_university_from_id(g.db, row.university_id).name
            )
        student_info["universityname"] = universityname
        student_info["status"] = "success"
        return json.dumps(student_info)
    return jsonify(status="false")


@validate_user_login
@allow_cross_domain
def get_user_detail_info():
    if request.method == "GET":
        student_id = request.args.get("studentid", 0, int)
        student_info = dict()
        offers = list()
        login_user_id = session.get("user_id")
        user_info = User.get_user_info(g.db,student_id)
        if login_user_id is None:
            login_user_id = -1
        for row in Offer.get_offer_student_info(g.db, student_id):
            offer_info = dict()

            for row_un in University.get_university_info(g.db,str(row.university_id)):
                offer_info["universityname"] = row_un.name
                offer_info["universityid"] = row_un.id
                offer_info["logo"] = get_university_logo(row_un.name)
                offer_info["twodimcode"] = row.wechat
            for row_ma in Major.get_major_info_by_id(g.db, row.major_id):
                offer_info["majorname"] = row_ma.name
            offer_info["grade"] = row.grade
            offer_info["offertype"] = row.offer_type
            if row.scholarship is not None:
                offer_info["scholarship"] = \
                    str(row.scholarship) + row.scholarship_type
                #offer_info["scholarship"] = None
            offers.append(offer_info)
        student_info["offers"] = offers
        compares = []
        compares_info = {}
        for row_co in Compare.get_compare_user_id(g.db, student_id):
            compares_info["compareid"] = row_co.id
            compareslist = list()
            compares_un = {}
            for row_ci in CompareInfo.get_compare_info(g.db, row_co.id):
                for row_un in University.get_university_info(
                        g.db, row_ci.university_id
                ):
                    compares_un["universityname"] = row_un.name
                    compares_un["universityid"] = row_un.id
                    compares_un["logo"] = row_un.schoollogo
                for row_ma in CompareInfo.get_compare_info(g.db,
                                                           row_ci.major_id):
                    compares_un["majorname"] = row_ma.name
                    compares_un["supportnum"] = row_ci.supportnum
                compares_un["offernum"] = Offer.get_offer_num(
                    g.db, row_ci.university_id
                )
                compareslist.append(compares_un)
                compares_un = {}
            compares_info["comparelist"] = compareslist
            compares.append(compares_info)
        student_info["compares"] = compares
        user = User.get_user_info(g.db, student_id)
        student_info["fannum"] = UserFollow.get_follow_count_user(g.db,
                                                                  student_id)
        if user is None:
            student_info["description"] = ""
            student_info["bginf"] = ""
        else:
            student_info["description"] = user.description
            student_info["bginf"] = user.bginf
        if int(login_user_id) == int(student_id):
            student_info["self"] = "true"
            student_info["phone"] = user.phone
            student_info["email"] = user.email
        else:
            student_info["self"] = "false"
            student_info["phone"] = ""
            student_info["email"] = ""

        message = list()
        for row_meg in Message.get_message_user(g.db, student_id):
            message_dict = dict()
            message_dict["messageid"] = row_meg.id
            user_id = row_meg.user_id
            user = User.get_user_info(g.db, user_id)
            if user is None:
                message.append(message_dict)
            else:
                message_dict["pic"] = user.pic
                message_dict["name"] = user.username
                message_dict["studentid"] = user_id
                message_dict["content"] = row_meg.message
                message_dict["time"] = get_timestamp(row_meg.create_time)
                message.append(message_dict)
        student_info["messages"] = message
        u"""这个位置的关注状态逻辑有点奇葩，以后要多注意"""
        follow_status = UserFollow.get_follow_to_user(g.db,
                                                      login_user_id,
                                                      student_id)
        if follow_status is not None:
            student_info["followed"] = "true"
        else:
            student_info["followed"] = "false"
        follows_list = list()
        for row_follow in UserFollow.get_follow_id(g.db, student_id):
            follows = dict()
            follow_user_id = row_follow.follow_user_id
            user = User.get_user_info(g.db, follow_user_id)
            if user is None:
                follows_list.append(follows)
            else:
                follows["name"] = user.username
                follows["pic"] = user.pic
                follows["studentid"] = follow_user_id
                follows_list.append(follows)
        student_info["follows"] = follows_list
        student_info["status"] = "success"
        score = Score.get_user_score(g.db, student_id)
        if score is None:
            return jsonify(student_info)

        sub_list = list()
        for row in Stasub.get_sub(g.db,student_id):
            sub = dict()
            sub["id"] = row.id
            sub["grade"] = row.grade
            sub_list.append(sub)
        GREmore = dict()

        GREmore["sub"] =sub_list
        GREmore["V"] = score.GRE_v
        GREmore["Q"] = score.GRE_q
        GREmore["AW"] = score.GRE_aw
        GREmore["total"] = user_info.GRE
        if student_info.get("v") != 0:
            student_info["GREmore"] = GREmore
        GMATmore = dict()
        GMATmore["V"] = score.GMAT_v
        GMATmore["Q"] = score.GMAT_q
        GMATmore["AW"] = score.GMAT_aw
        GMATmore["IR"] = score.GMAT_ir
        GMATmore["total"] = user_info.GMAT
        if GMATmore.get("V") != 0:
            student_info["GMATmore"] = GMATmore
        IELTSmore = dict()
        IELTSmore["R"] = score.IELTS_r
        IELTSmore["L"] = score.IELTS_l
        IELTSmore["S"] = score.IELTS_s
        IELTSmore["W"] = score.IELTS_w
        IELTSmore["total"] = user_info.IELTS
        if IELTSmore.get("R") != 0:
            student_info["IELTSmore"] = IELTSmore
        TOEFLmore = dict()
        TOEFLmore["R"] = score.TOEFL_r
        TOEFLmore["L"] = score.TOEFL_l
        TOEFLmore["S"] = score.TOEFL_s
        TOEFLmore["W"] = score.TOEFL_w
        TOEFLmore["total"] = user_info.TOEFL
        if TOEFLmore.get("R") != 0:
            student_info["TOEFLmore"] = TOEFLmore
        SATmore = dict()
        SATmore["CR"] = score.SAT_cr
        SATmore["W"] = score.SAT_w
        SATmore["M"] = score.SAT_m
        SATmore["total"] = user_info.SAT
        if SATmore.get("W") != 0:
            student_info["SATmore"] = SATmore
        GMATmore = dict()
        GMATmore["V"] = score.GMAT_v
        GMATmore["Q"] = score.GMAT_q
        GMATmore["AW"] = score.GMAT_aw
        GMATmore["IR"] = score.GMAT_ir
        GMATmore["total"] = user_info.GMAT
        if GMATmore.get("V") != 0:
            student_info["GMATmore"] = GMATmore
        coupons = dict()

        print user_info.account,user.active,
        if user_info.active == 1 and user_info.account is not None:
            coupons["code"] = user_info.coupon
            coupons["account"] = user_info.account
        elif user_info.active == 2 and user_info.account is not None:
            coupons["code"] = None
            coupons["account"] = user_info.account
        else:
            coupons["code"] = None
            coupons["account"] = None
        student_info["coupons"] = coupons

        return json.dumps(student_info)


@allow_cross_domain
def get_user_in_university():
    if request.method == "POST":
        data = request.form
        #return jsonify(status="success")
        #data = json.loads(request.data)
        user_id = session.get("user_id")
        user = User.get_user_info(g.db,user_id)
        user_type = -1
        if user:
            user_type = user.type

        university_id = data.get("universityid")
        faculty_id = data.get("facultyid")
        major_id = data.get("majorid")
        GPA_to = data.get("GPA[to]",0.0,float)
        GPA_form = data.get("GPA[from]",1000,float)
        TOEFL_to = request.form.get("TOEFL[to]",0.0,float)
        TOEFL_form = request.form.get("TOEFL[from]",10000,float)


        IELTS_to= request.form.get("IELTS[to]",0.0,float)
        IELTS_form = request.form.get("IELTS[from]",10000,float)
        if TOEFL_to != 0.0 and TOEFL_form != 10000:
            IELTS_to = 0.0
            IELTS_form = 0.0
        elif IELTS_to != 0.0 and IELTS_form != 10000:
            TOEFL_to = 0.0
            TOEFL_form = 0.0

        GRE_to = request.form.get("GRE[to]",0.0,float)
        GRE_form = request.form.get("GRE[from]",10000,float)
        GMAT_to = request.form.get("GMAT[to]",0.0,float)
        GMAT_form = request.form.get("GMAT[from]",10000,float)
        if GRE_to != 0.0 and GRE_form != 10000:
            GMAT_to = 0.0
            GMAT_form =0.0
        elif GMAT_to != 0.0 and GMAT_form != 10000:
            GRE_to = 0.0
            GRE_form = 0.0

        grade = request.form.get("grade")
        print grade
        page = data.get("page")

        compares = {}
        compare_list = []
        page_list = []

        if faculty_id is not None:
            if major_id is None:
                major_list = dict()
                info = list()
                for row_major in Major.get_major_from_faculty(g.db,university_id,faculty_id):
                    student_list = []
                    student = {}
                    for row in Offer.get_user_id_from_university(g.db,
                                                         university_id,
                                                         row_major.id,
                                                         user_type,
                                                         grade):
                        user = User.get_user_info(g.db,row.user_id)
                        if user:

                            if get_compare_score(GPA_to,GPA_form,user.GPA) and \
                                get_compare_score(TOEFL_to,TOEFL_form,user.TOEFL) and \
                                get_compare_score(IELTS_to,IELTS_form,user.IELTS) and \
                                get_compare_score(GRE_to,GRE_form,user.GRE) and \
                                get_compare_score(GMAT_to,GMAT_form,user.GMAT):

                                student_list.append(row.user_id)
                    student["studentlist"] = student_list
                    student["majorid"] = row_major.id
                    student["majorname"] = row_major.name
                    page = len(student_list) / 15
                    student["more"] = ""
                    if int(page) > 1:
                        student["more"] = "true"
                    if len(student.get("studentlist")) > 0:
                        info.append(student)

                major_list["majorlist"] = info
                major_list["status"] = "success"
                return json.dumps(major_list)
            elif major_id is not None:
                student_list = []
                for row in Offer.get_user_id_from_university(g.db,
                                                        university_id,
                                                        major_id,
                                                        user_type,
                                                        grade):
                    user = User.get_user_info(g.db,row.user_id)
                    if user:

                        if get_compare_score(GPA_to,GPA_form,user.GPA) and \
                                get_compare_score(TOEFL_to,TOEFL_form,user.TOEFL) and \
                                get_compare_score(IELTS_to,IELTS_form,user.IELTS) and \
                                get_compare_score(GRE_to,GRE_form,user.GRE) and \
                                get_compare_score(GMAT_to,GMAT_form,user.GMAT):

                            student_list.append(row.user_id)
        else:
            student_list = []
            for row in Offer.get_user_id_from_university(g.db,
                                                        university_id,
                                                        major_id,
                                                        user_type,
                                                        grade):
                user = User.get_user_info(g.db,row.user_id)
                if user:

                    if get_compare_score(GPA_to,GPA_form,user.GPA) and \
                                get_compare_score(TOEFL_to,TOEFL_form,user.TOEFL) and \
                                get_compare_score(IELTS_to,IELTS_form,user.IELTS) and \
                                get_compare_score(GRE_to,GRE_form,user.GRE) and \
                                get_compare_score(GMAT_to,GMAT_form,user.GMAT):

                        student_list.append(row.user_id)
            student = dict()
            student["studentlist"] = list(set(student_list))
            page = len(student_list) / 15
            student["more"] = ""
            if int(page) > 1:
                student["more"] = "true"
            student["status"] = "success"
            return json.dumps(student)

        return jsonify(status="false")


@validate_user_login
def update_user_bginf():
    u"""修改个人背景信息"""
    if request.method == "POST":
        bginf = request.form.get("bginf")
        user_id = session.get("user_id")
        User.update_user_bginf(g.db, user_id=user_id, bginf=bginf)
        return jsonify(status="success")
    return jsonify(status="false")


@validate_user_login
def get_user_base_info():
    u"""获取个人信息，用来更细资料"""
    if request.method == "GET":

        user_id = session.get("user_id")
        user = User.get_user_info(g.db, user_id)
        user_info = dict()
        user_info["status"] = "success"
        data = dict()
        data["type"] = str(user.type)
        data["bginf"] = user.bginf
        user_info["data"] = data
        score = Score.get_user_score(g.db, user_id)
        if score is None:
            return jsonify(user_info)
        GREmore = dict()
        #GREmore["sub"] = list()
        sub_list = list()

        data["GREmore"] = None
        data["TOEFLmore"] = None

        data["SATmore"] = None
        data["IELTSmore"] = None

        data["GMATmore"] = None
        for sub in Stasub.get_sub(g.db,user_id):
            sub_dict = dict()
            sub_dict["id"] = sub.sub_id
            sub_dict["grade"] = sub.grade
            sub_list.append(sub_dict)

        GREmore["sub"] = sub_list
        GREmore["V"] = score.GRE_v
        GREmore["Q"] = score.GRE_q
        GREmore["AW"] = score.GRE_aw
        GREmore["total"] = user.GRE

        if GREmore.get("V") != 0:

            data["GREmore"] = GREmore
        TOEFLmore = dict()
        TOEFLmore["R"] = score.TOEFL_r
        TOEFLmore["L"] = score.TOEFL_l
        TOEFLmore["S"] = score.TOEFL_s
        TOEFLmore["W"] = score.TOEFL_w
        TOEFLmore["total"] = user.TOEFL
        if TOEFLmore.get("W") != 0:
            data["TOEFLmore"] = TOEFLmore
        SATmore = dict()
        SATmore["sub"] = sub_list
        SATmore["CR"] = score.SAT_cr
        SATmore["W"] = score.SAT_w
        SATmore["M"] = score.SAT_m
        SATmore["total"] = user.SAT
        if SATmore.get("CR") != 0:
            data["SATmore"] = SATmore
        IELTSmore = dict()
        IELTSmore["R"] = score.IELTS_r
        IELTSmore["L"] = score.IELTS_l
        IELTSmore["S"] = score.IELTS_s
        IELTSmore["W"] = score.IELTS_w
        IELTSmore["total"] = user.IELTS
        if IELTSmore.get("R") != 0:
            data["IELTSmore"] = IELTSmore
        GMATmore = dict()
        GMATmore["V"] = score.GMAT_v
        GMATmore["Q"] = score.GMAT_q
        GMATmore["AW"] = score.GMAT_aw
        GMATmore["IR"] = score.GMAT_ir
        GMATmore["total"] = user.GMAT
        if GMATmore.get("V") != 0:
            data["GMATmore"] = GMATmore

        return jsonify(user_info)
    return jsonify(status="false")

@validate_user_login
def edit_user_info_page():
    if request.method == "GET":
        user_id = session.get("user_id")
        user = User.get_user_info(g.db,user_id)

        if user is None:
            return jsonify(status="false")
        user_info = dict()
        user_info["status"] = "success"
        user_info["type"] = str(user.type)
        user_info["engname"] = user.username
        user_info["pic"] = user.pic
        user_info["phonenum"] = user.phone
        user_info["email"] = user.email
        #user_info["password"] = user.password
        user_info["universityname"] = user.prevuniversity
        user_info["majorname"] = user.prevmajor
        score = Score.get_user_score(g.db, user_id)
        if score is None:
            return json.dumps(user_info)
        GREmore = dict()
        sub_list = list()

        for sub in Stasub.get_sub(g.db,user_id):
            sub_dict = dict()
            sub_dict["id"] = sub.sub_id
            sub_dict["grade"] = sub.grade
            sub_list.append(sub_dict)

        GREmore["sub"] = sub_list
        GREmore["V"] = score.GRE_v
        GREmore["Q"] = score.GRE_q
        GREmore["AW"] = score.GRE_aw
        GREmore["total"] = user.GRE
        if GREmore.get("V") != 0:
            user_info["GREmore"] = GREmore
        TOEFLmore = dict()
        TOEFLmore["R"] = score.TOEFL_r
        TOEFLmore["L"] = score.TOEFL_l
        TOEFLmore["S"] = score.TOEFL_s
        TOEFLmore["W"] = score.TOEFL_w
        TOEFLmore["total"] = user.TOEFL
        if TOEFLmore.get("R") != 0:
            user_info["TOEFLmore"] = TOEFLmore
        SATmore = dict()
        SATmore["sub"] = sub_list
        SATmore["CR"] = score.SAT_cr
        SATmore["W"] = score.SAT_w
        SATmore["M"] = score.SAT_m
        SATmore["total"] = user.SAT
        if SATmore.get("M") != 0:
            user_info["SATmore"] = SATmore
        IELTSmore = dict()
        IELTSmore["R"] = score.IELTS_r
        IELTSmore["L"] = score.IELTS_l
        IELTSmore["S"] = score.IELTS_s
        IELTSmore["W"] = score.IELTS_w
        IELTSmore["total"] = user.IELTS
        if IELTSmore.get("R") != 0:
            user_info["IELTSmore"] = IELTSmore

        GMATmore = dict()
        GMATmore["V"] = score.GMAT_v
        GMATmore["Q"] = score.GMAT_q
        GMATmore["AW"] = score.GMAT_aw
        GMATmore["IR"] = score.GMAT_ir
        GMATmore["total"] = user.GMAT
        if GMATmore.get("V") != 0:
            user_info["GMATmore"] = GMATmore
        return json.dumps(user_info)
    return jsonify(status="success")


@validate_user_login
def update_user_info():
    U"""用户更新资料"""
    if request.method == "POST":
        user_id = session.get("user_id")
        phone = request.form.get("phonenum")
        username = request.form.get("engname")
        email = request.form.get("email")
        pic = request.form.get("pic")
        print request.form
        phone = request.form.get("phonenum")
        check_num = request.form.get("checknum")
        user = User.get_user_info(g.db,user_id)
        if check_num or check_num == "":
            print user.checknum,check_num,checknum_timeout(user.checknum_time)
            if check_num == "":
                return jsonify(status="checknum_error")
            if user.checknum == int(check_num) and checknum_timeout(user.checknum_time):
                User.update_user_phone(g.db,user.id,phone,user.phone_old,)
            else:
                return jsonify(status="checknum_error")
        if request.form.get("passwordold"):
            password = request.form.get("password")
            passwordold = request.form.get("passwordold")
            if not User.change_password_old(g.db,user_id,
                                            set_password_salt(password),
                                            set_password_salt(passwordold)):

                return jsonify(status="false")
        if pic is not None:
            User.update_user_pic(g.db,user_id,pic)

        Stasub.del_sub(g.db,user_id)
        if request.form.get("GRE[sub][0][id]"):
            num = 0
            while True:
                if request.form.get("GRE[sub]["+str(num)+"][id]"):
                    sub_id = request.form.get("GRE[sub]["+str(num)+"][id]",0,int)
                    grade = request.form.get("GRE[sub]["+str(num)+"][grade]",0,int)
                    sub_type = 0
                    if sub_id > 10:
                        sub_type = 1
                    Stasub.set_sub(g.db, sub_id=sub_id, grade=grade,
                                   sub_type=sub_type, user_id=user_id)
                    num += 1
                else:
                    break

        #Stasub.del_sub(g.db,user_id)
        if request.form.get("SAT[sub][0][grade]"):
            num = 0
            while True:
                if request.form.get("SAT[sub]["+str(num)+"][id]"):
                    sub_id = request.form.get("SAT[sub]["+str(num)+"][id]",0,int)
                    grade = request.form.get("SAT[sub]["+str(num)+"][grade]",0,int)
                    sub_type = 0
                    if sub_id >10:
                        sub_type = 1
                    Stasub.set_sub(g.db, sub_id=sub_id, grade=grade,
                                   sub_type=sub_type, user_id=user_id)
                    num += 1
                else:
                    break


        prevmajor = request.form.get("majorid")
        prevuniversity = request.form.get("universityid")
        User.update_user_info(g.db, user_id=user_id, username=username,
                              email=email,
                              prevuniversity=prevuniversity,prevmajor=prevmajor)
        if request.form.get("IELTS[R]") is not None:
            LELTSmoreR = request.form.get("IELTS[R]",float)
            LELTSmoreL = request.form.get("IELTS[L]",float)
            LELTSmoreS = request.form.get("IELTS[S]",float)
            LELTSmoreW = request.form.get("IELTS[W]",float)
            sub_TELTS = request.form.get("IELTS[total]", float)

            if request.form.get("GRE[V]") is not None:
                GREmoreV = request.form.get("GRE[V]",int)
                GREmoreQ = request.form.get("GRE[Q]",int)
                GREmoreAW = request.form.get("GRE[AW]",float)
                sub_GRE = request.form.get("GRE[total]", int)
                User.update_user_score(g.db,user_id, gre=sub_GRE,
                                       lelts=sub_TELTS)
                Score.set_user_info(connection=g.db, user_id=user_id,

                                    IELTS_r=LELTSmoreR,
                                    IELTS_l=LELTSmoreL,
                                    IELTS_s=LELTSmoreS,
                                    IELTS_w=LELTSmoreW,
                                    GRE_v=GREmoreV,
                                    GRE_q=GREmoreQ,
                                    GRE_aw=GREmoreAW

                                    )
            elif request.form.get("SAT[M]"):
                sat_m = request.form.get("SAT[M]", int)
                sat_cr = request.form.get("SAT[CR]", int)
                sat_w = request.form.get("SAT[W]", int)
                sub_sat= request.form.get("SAT[total]", int)
                User.update_user_score(g.db,user_id=user_id,
                                       lelts=sub_TELTS,
                                       sat=sub_sat)
                Score.set_user_info(connection=g.db,
                                    user_id=user_id,
                                    IELTS_r=LELTSmoreR,
                                    IELTS_l=LELTSmoreL,
                                    IELTS_s=LELTSmoreS,
                                    IELTS_w=LELTSmoreW,
                                    SAT_m=sat_m,
                                    SAT_w=sat_w,
                                    SAT_cr=sat_cr
                )

            else:
                GMATmoreV = request.form.get("GMAT[V]", int)
                GMATmoreQ = request.form.get("GMAT[Q]", int)
                GMATmoreAW = request.form.get("GMAT[AW]", float)
                GMATmoreIR = request.form.get("GMAT[IR]", int)
                sub_GMAT = request.form.get("GMAT[total]",  int)
                User.update_user_score(g.db, user_id=user_id,
                                       lelts=sub_TELTS, GMAT=sub_GMAT)
                Score.set_user_info(connection=g.db,
                                    user_id=user_id,
                                    IELTS_r=LELTSmoreR,
                                    IELTS_l=LELTSmoreL,
                                    IELTS_s=LELTSmoreS,
                                    IELTS_w=LELTSmoreW,
                                    GMAT_v=GMATmoreV,
                                    GMAT_q=GMATmoreQ,
                                    GMAT_aw=GMATmoreAW,
                                    GMAT_ir=GMATmoreIR

                                    )


        elif request.form.get("TOEFL[R]") is not None:

            TOEFLmoreR = request.form.get("TOEFL[R]",int)
            TOEFLmoreL = request.form.get("TOEFL[L]",int)
            TOEFLmoreS = request.form.get("TOEFL[S]",int)
            TOEFLmoreW = request.form.get("TOEFL[W]",int)
            sub_TOEFL = request.form.get("TOEFL[total]", int)
            if request.form.get("GRE[V]") is not None:
                GREmoreV = request.form.get("GRE[V]", int)
                GREmoreQ = request.form.get("GRE[Q]", int)
                GREmoreAW = request.form.get("GRE[AW]", float)
                sub_GRE = request.form.get("GRE[total]", int)
                User.update_user_score(g.db, user_id=user_id, gre=sub_GRE,
                                       toefl=sub_TOEFL)
                Score.set_user_info(connection=g.db,user_id=user_id,
                                    TOEFL_r =TOEFLmoreR,
                                    TOEFL_l =TOEFLmoreL,
                                    TOEFL_s =TOEFLmoreS,
                                    TOEFL_w =TOEFLmoreW,
                                    GRE_v=GREmoreV,
                                    GRE_q=GREmoreQ,
                                    GRE_aw=GREmoreAW

                                    )
            elif request.form.get("SAT[M]"):
                sat_m = request.form.get("SAT[M]", 0, int)
                sat_cr = request.form.get("SAT[CR]", 0, int)
                sat_w = request.form.get("SAT[W]", 0, int)
                sub_sat= request.form.get("SAT[total]", 0, int)

                User.update_user_score(g.db,user_id=user_id,
                                       toefl=sub_TOEFL,
                                       sat=sub_sat)
                Score.set_user_info(connection=g.db,
                                    user_id=user_id,
                                    TOEFL_r=TOEFLmoreR,
                                    TOEFL_l=TOEFLmoreL,
                                    TOEFL_s=TOEFLmoreS,
                                    TOEFL_w=TOEFLmoreW,
                                    SAT_m=sat_m,
                                    SAT_w=sat_w,
                                    SAT_cr=sat_cr
                )
            else:
                GMATmoreV = request.form.get("GMAT[V]",int)
                GMATmoreQ = request.form.get("GMAT[Q]",int)
                GMATmoreAW = request.form.get("GMAT[AW]",float)
                GMATmoreIR = request.form.get("GMAT[IR]",int)
                sub_GMAT = request.form.get("GMAT[total]",int)

                User.update_user_score(g.db, user_id=user_id,
                                       toefl=sub_TOEFL, GMAT=sub_GMAT)
                Score.set_user_info(connection=g.db,user_id=user_id,

                                    TOEFL_r =TOEFLmoreR,
                                    TOEFL_l =TOEFLmoreL,
                                    TOEFL_s =TOEFLmoreS,
                                    TOEFL_w =TOEFLmoreW,
                                    GMAT_v=GMATmoreV,
                                    GMAT_q=GMATmoreQ,
                                    GMAT_aw=GMATmoreAW,
                                    GMAT_ir=GMATmoreIR
                                    )
        User.set_user_active(g.db,user_id)
        return jsonify(status="success")
    return jsonify(status="false")

@validate_user_login
def update_user_description():
    if request.method == "POST":
        description = request.form.get("description")
        user_id = session.get("user_id")
        User.update_user_description(g.db,user_id,description)
        return jsonify(status="success")
    return jsonify(status="false")




