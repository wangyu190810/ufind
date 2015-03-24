# -*-coding:utf-8-*-
__author__ = 'wangyu'

from flask import g, jsonify, request, session
import json

from mysite.model.user import User, UserFollow
from mysite.view.base import allow_cross_domain, get_timestamp, \
    validate_user_login,get_university_logo,get_university_twodim,\
    get_GMAT, get_gre, get_TELTS, get_Total,get_SAT,get_compare_score
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

        if login_user_id is None:
            login_user_id = -1
        for row in Offer.get_offer_student_info(g.db, student_id):
            offer_info = dict()
            for row_un in University.get_university_info(g.db,
                                                         row.university_id):
                offer_info["universityname"] = row_un.name
                offer_info["logo"] = get_university_logo(row_un.name)
                offer_info["twodimcode"] = get_university_twodim(row_un.name)
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
        if student_info.get("v") != 0:
            student_info["GREmore"] = GREmore
        GMATmore = dict()
        GMATmore["V"] = score.GMAT_v
        GMATmore["Q"] = score.GMAT_q
        GMATmore["AW"] = score.GMAT_aw
        GMATmore["IR"] = score.GMAT_ir
        if GMATmore.get("V") != 0:
            student_info["GMATmore"] = GMATmore
        IELTSmore = dict()
        IELTSmore["R"] = score.IELTS_r
        IELTSmore["L"] = score.IELTS_l
        IELTSmore["S"] = score.IELTS_s
        IELTSmore["W"] = score.IELTS_w
        if IELTSmore.get("R") != 0:
            student_info["IELTSmore"] = IELTSmore
        TOEFLmore = dict()
        TOEFLmore["R"] = score.TOEFL_r
        TOEFLmore["L"] = score.TOEFL_l
        TOEFLmore["S"] = score.TOEFL_s
        TOEFLmore["W"] = score.TOEFL_w
        if TOEFLmore.get("R") != 0:
            student_info["TOEFLmore"] = TOEFLmore
        SATmore = dict()
        SATmore["CR"] = score.SAT_cr
        SATmore["W"] = score.SAT_w
        SATmore["M"] = score.SAT_m
        if SATmore.get("W") != 0:
            student_info["SATmore"] = SATmore
        GMATmore = dict()
        GMATmore["V"] = score.GMAT_v
        GMATmore["Q"] = score.GMAT_q
        GMATmore["AW"] = score.GMAT_aw
        GMATmore["IR"] = score.GMAT_ir
        if GMATmore.get("V") != 0:
            student_info["GMATmore"] = GMATmore

        return json.dumps(student_info)


@allow_cross_domain
def get_user_in_university():
    if request.method == "POST":
        print request.form
        data = request.form
        #return jsonify(status="success")
        #data = json.loads(request.data)

        university_id = data.get("universityid")
        faculty_id = data.get("facultyid")
        major_id = data.get("majorid")
        GPA_to = data.get("GPA[to]",0.0,float)
        GPA_form = data.get("GPA[from]",0.0,float)
        TOEFL_to = request.form.get("TOEFL[to]",0.0,float)
        TOEFL_form = request.form.get("TOEFL[from]",0.0,float)
        GER_to = request.form.get("GRE[to]",0.0,float)
        GER_form = request.form.get("GRE[from]",0.0,float)
        TOEFL_form = request.form.get("TOEFL[from]")
        TOEFL_form = request.form.get("TOEFL[from]")#   SAT = data["SAT"]
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
                                                         row_major.id):
                        user = User.get_user_info(g.db,row.user_id)
                        print user
                        if user:
                            print GPA_to
                            print GPA_form
                            print get_compare_score(GPA_to,GPA_form,user.GPA)
                            if GPA_to != 0.0:
                                if TOEFL_to != 0.0:
                                    if GER_to != 0.0:
                                        if get_compare_score(GPA_to,GPA_form,user.GPA) and \
                                            get_compare_score(TOEFL_to,TOEFL_form,user.TOEFL) and\
                                            get_compare_score(GER_to,GER_form,user.GRE):

                                                student_list.append(row.user_id)
                                    elif get_compare_score(GPA_to,GPA_form,user.GPA) and \
                                            get_compare_score(TOEFL_to,TOEFL_form,user.TOEFL):

                                        student_list.append(row.user_id)
                                elif get_compare_score(GPA_to,GPA_form,user.GPA):
                                    student_list.append(row.user_id)
                            else:
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
                                                        major_id):
                    user = User.get_user_info(g.db,row.user_id)
                    print user
                    if user:
                        print GPA_to
                        print GPA_form
                        print get_compare_score(GPA_to,GPA_form,user.GPA)
                        if GPA_to != 0.0:
                            if TOEFL_to != 0.0:
                                if GER_to != 0.0:
                                    if get_compare_score(GPA_to,GPA_form,user.GPA) and \
                                        get_compare_score(TOEFL_to,TOEFL_form,user.TOEFL) and\
                                        get_compare_score(GER_to,GER_form,user.GRE):

                                                student_list.append(row.user_id)
                                elif get_compare_score(GPA_to,GPA_form,user.GPA) and \
                                        get_compare_score(TOEFL_to,TOEFL_form,user.TOEFL):

                                    student_list.append(row.user_id)
                            elif get_compare_score(GPA_to,GPA_form,user.GPA):
                                student_list.append(row.user_id)
                        else:
                            student_list.append(row.user_id)
                    student_list.append(row.user_id)

            student = dict()
            student["studentlist"] = student_list
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
        print sub_list
        GREmore["sub"] = sub_list
        GREmore["V"] = score.GRE_v
        GREmore["Q"] = score.GRE_q
        GREmore["AW"] = score.GRE_aw
        if GREmore.get("V") != 0:

            data["GREmore"] = GREmore
        TOEFLmore = dict()
        TOEFLmore["R"] = score.TOEFL_r
        TOEFLmore["L"] = score.TOEFL_l
        TOEFLmore["S"] = score.TOEFL_s
        TOEFLmore["W"] = score.TOEFL_w
        if TOEFLmore.get("W") != 0:
            data["TOEFLmore"] = TOEFLmore
        SATmore = dict()
        SATmore["sub"] = sub_list
        SATmore["CR"] = score.SAT_cr
        SATmore["W"] = score.SAT_w
        SATmore["M"] = score.SAT_m

        if SATmore.get("CR") != 0:
            data["SATmore"] = SATmore
        IELTSmore = dict()
        IELTSmore["R"] = score.IELTS_r
        IELTSmore["L"] = score.IELTS_l
        IELTSmore["S"] = score.IELTS_s
        IELTSmore["W"] = score.IELTS_w
        if IELTSmore.get("R") != 0:
            data["IELTSmore"] = IELTSmore
        GMATmore = dict()
        GMATmore["V"] = score.GMAT_v
        GMATmore["Q"] = score.GMAT_q
        GMATmore["AW"] = score.GMAT_aw
        GMATmore["IR"] = score.GMAT_ir
        if GMATmore.get("V") != 0:
            data["GMATmore"] = GMATmore

        return jsonify(user_info)
    return jsonify(status="false")

@validate_user_login
def edit_user_info_page():
    if request.method == "GET":
        user_id = session.get("user_id")
        user = User.get_user_info(g.db,user_id)
        print user
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
        print sub_list
        GREmore["sub"] = sub_list
        GREmore["V"] = score.GRE_v
        GREmore["Q"] = score.GRE_q
        GREmore["AW"] = score.GRE_aw
        if GREmore.get("V") != 0:
            user_info["GREmore"] = GREmore
        TOEFLmore = dict()
        TOEFLmore["R"] = score.TOEFL_r
        TOEFLmore["L"] = score.TOEFL_l
        TOEFLmore["S"] = score.TOEFL_s
        TOEFLmore["W"] = score.TOEFL_w
        if TOEFLmore.get("R") != 0:
            user_info["TOEFLmore"] = TOEFLmore
        SATmore = dict()
        SATmore["sub"] = sub_list
        SATmore["CR"] = score.SAT_cr
        SATmore["W"] = score.SAT_w
        SATmore["M"] = score.SAT_m
        if SATmore.get("M") != 0:
            user_info["SATmore"] = SATmore
        IELTSmore = dict()
        IELTSmore["R"] = score.IELTS_r
        IELTSmore["L"] = score.IELTS_l
        IELTSmore["S"] = score.IELTS_s
        IELTSmore["W"] = score.IELTS_w
        if IELTSmore.get("R") != 0:
            user_info["IELTSmore"] = IELTSmore
        print user_info
        GMATmore = dict()
        GMATmore["V"] = score.GMAT_v
        GMATmore["Q"] = score.GMAT_q
        GMATmore["AW"] = score.GMAT_aw
        GMATmore["IR"] = score.GMAT_ir
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
        if request.form.get("checknum"):
            pass
        if request.form.get("passwordold"):
            password = request.form.get("password")
            passwordold = request.form.get("passwordold")
            if not User.change_password_old(g.db,user_id,password,passwordold):
                print "123124"
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
                              phone=phone, email=email,
                              prevuniversity=prevuniversity,prevmajor=prevmajor)
        if request.form.get("IELTS[R]") is not None:
            LELTSmoreR = request.form.get("IELTS[R]",0,int)
            LELTSmoreL = request.form.get("IELTS[L]",0,int)
            LELTSmoreS = request.form.get("IELTS[S]",0,int)
            LELTSmoreW = request.form.get("IELTS[W]",0,int)
            sub_TELTS = get_TELTS(LELTSmoreS, LELTSmoreL, LELTSmoreR,
                                  LELTSmoreW)
            if request.form.get("GRE[V]") is not None:
                GREmoreV = request.form.get("GRE[V]",0,int)
                GREmoreQ = request.form.get("GRE[Q]",0,int)
                GREmoreAW = request.form.get("GRE[AW]",0,int)
                sub_GRE = get_gre(GREmoreV, GREmoreQ)
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
                sat_m = request.form.get("SAT[M]", 0, int)
                sat_cr = request.form.get("SAT[CR]", 0, int)
                sat_w = request.form.get("SAT[W]", 0, int)
                sub_sat = get_SAT(sat_cr,sat_w,sat_m)
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
                GMATmoreV = request.form.get("GMAT[V]",0,int)
                GMATmoreQ = request.form.get("GMAT[Q]",0,int)
                GMATmoreAW = request.form.get("GMAT[AW]",0,int)
                GMATmoreIR = request.form.get("GMAT[IR]",0,int)
                sub_GMAT = get_GMAT(GMATmoreV, GMATmoreQ)
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
            print request.form
            TOEFLmoreR = request.form.get("TOEFL[R]",0,int)
            TOEFLmoreL = request.form.get("TOEFL[L]",0,int)
            TOEFLmoreS = request.form.get("TOEFL[S]",0,int)
            TOEFLmoreW = request.form.get("TOEFL[W]",0,int)
            sub_TOEFL = get_Total(TOEFLmoreL, TOEFLmoreR, TOEFLmoreS,
                                  TOEFLmoreW)
            if request.form.get("GRE[V]") is not None:
                GREmoreV = request.form.get("GRE[V]",0,int)
                GREmoreQ = request.form.get("GRE[Q]",0,int)
                GREmoreAW = request.form.get("GRE[AW]",0,int)
                sub_GRE = get_gre(GREmoreV, GREmoreQ)
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
                sub_sat = get_SAT(sat_cr,sat_w,sat_m)
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
                GMATmoreV = request.form.get("GMAT[V]",0,int)
                GMATmoreQ = request.form.get("GMAT[Q]",0,int)
                GMATmoreAW = request.form.get("GMAT[AW]",0,int)
                GMATmoreIR = request.form.get("GMAT[IR]",0,int)
                sub_GMAT = get_GMAT(GMATmoreV, GMATmoreQ)
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




