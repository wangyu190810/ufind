# -*-coding:utf-8-*-
__author__ = 'wangyu'

from flask import g, jsonify, request, session
import json

from mysite.model.user import User, UserFollow
from mysite.view.base import allow_cross_domain, get_timestamp, \
    validate_user_login,get_university_logo,get_university_twodim
from mysite.model.offer import Offer
from mysite.model.university import University
from mysite.model.major import Major
from mysite.model.compare import CompareInfo, Compare
from mysite.model.message import Message
from mysite.model.score import Score


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
            else:
                offer_info["scholarship"] = None
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
            follows["name"] = user.username
            follows["pic"] = user.pic
            follows["studentid"] = follow_user_id
            follows_list.append(follows)
        student_info["follows"] = follows_list
        student_info["status"] = "success"
        score = Score.get_user_score(g.db, student_id)
        if score is None:
            return jsonify(student_info)
        GREmore = dict()
        GREmore["sub"] = list()
        GREmore["V"] = score.GRE_v
        GREmore["Q"] = score.GRE_q
        GREmore["AW"] = score.GRE_aw
        student_info["GREmore"] = GREmore
        GMATmore = dict()
        GMATmore["V"] = score.GMAT_v
        GMATmore["Q"] = score.GMAT_q
        GMATmore["AW"] = score.GMAT_aw
        GMATmore["IR"] = score.GMAT_ir
        student_info["GMATmore"] = GMATmore
        IELTSmore = dict()
        IELTSmore["R"] = score.IELTS_r
        IELTSmore["L"] = score.IELTS_l
        IELTSmore["S"] = score.IELTS_s
        IELTSmore["W"] = score.IELTS_w
        student_info["IELTSmore"] = IELTSmore
        TOEFLmore = dict()
        TOEFLmore["R"] = score.TOEFL_r
        TOEFLmore["L"] = score.TOEFL_l
        TOEFLmore["S"] = score.TOEFL_s
        TOEFLmore["W"] = score.TOEFL_w
        student_info["TOEFLmore"] = TOEFLmore
        STAmore = dict()
        STAmore["CR"] = score.SAT_cr
        STAmore["W"] = score.SAT_w
        STAmore["M"] = score.SAT_m
        student_info["SATmore"] = STAmore

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
     #   grade = data.get("grade")
     #   GPA = data["GPA"]
     #   TOEFL = data["TOEFL"]
     #   GRE = data["GRE"]
     #   IELTS = data["IELTS"]
     #   GMAT = data["GMAT"]
     #   SAT = data["SAT"]
        page = data.get("page")
        compares = {}
        compare_list = []
        page_list = []
        student_list = []
        student = {}
        if faculty_id is not None:
            if major_id is None:
                major_id = None
            for row in Offer.get_user_id_from_university(g.db,
                                                         university_id,
                                                         major_id):
                student_list.append(row.user_id)
                student["studentlist"] = student_list
                page = len(student_list) / 15
            student["more"] = ""
            if int(page) > 1:
                student["more"] = "true"
            student["status"] = "success"

            return json.dumps(student)

        return jsonify(status="123")


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
        score = Score.get_user_score(g.db, user_id)
        if score is None:
            return jsonify(user_info)
        GREmore = dict()
        GREmore["sub"] = list()
        GREmore["V"] = score.GRE_v
        GREmore["Q"] = score.GRE_q
        GREmore["AW"] = score.GRE_aw
        data["GREmore"] = GREmore
        TOEFLmore = dict()
        TOEFLmore["R"] = score.TOEFL_r
        TOEFLmore["L"] = score.TOEFL_l
        TOEFLmore["S"] = score.TOEFL_s
        TOEFLmore["W"] = score.TOEFL_w
        data["TOEFLmore"] = TOEFLmore
        STAmore = dict()
        STAmore["CR"] = score.SAT_cr
        STAmore["W"] = score.SAT_w
        STAmore["M"] = score.SAT_m
        data["type"] = user.type
        data["bginf"] = user.bginf
        data["SATmore"] = STAmore
        user_info["data"] = data
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
        user_info["type"] = user.type
        user_info["engname"] = user.username
        user_info["pic"] = user.pic
        user_info["phonenum"] = user.phone
        user_info["email"] = user.email
        user_info["password"] = user.password
        user_info["universityname"] = user.prevuniversity
        user_info["majorname"] = user.prevmajor
        score = Score.get_user_score(g.db, user_id)
        if score is None:
            return json.dumps(user_info)
        GREmore = dict()
        GREmore["V"] = score.GRE_v
        GREmore["Q"] = score.GRE_q
        GREmore["AW"] = score.GRE_aw
        user_info["GREmore"] = GREmore
        TOEFLmore = dict()
        TOEFLmore["R"] = score.TOEFL_r
        TOEFLmore["L"] = score.TOEFL_l
        TOEFLmore["S"] = score.TOEFL_s
        TOEFLmore["W"] = score.TOEFL_w
        user_info["TOEFLmore"] = TOEFLmore
        STAmore = dict()
        STAmore["CR"] = score.SAT_cr
        STAmore["W"] = score.SAT_w
        STAmore["M"] = score.SAT_m
        user_info["STAmore"] = STAmore
        return json.dumps(user_info)
    return jsonify(status="success")


@validate_user_login
def update_user_info():
    U"""用户更新资料"""
    if request.method == "POST":
        print request.data
        print request.form
        user_id = session.get("user_id")
        phone = request.form.get("phonenum")
        username = request.form.get("engname")
        email = request.form.get("email")
        pic = request.form.get("pic")
        if pic is not None:
            User.update_user_pic(g.db,user_id,pic)
        prevmajor = request.form.get("majorid")
        prevuniversity = request.form.get("universityid")
        User.update_user_info(g.db, user_id=user_id, username=username,
                              phone=phone, email=email,
                              prevuniversity=prevuniversity,prevmajor=prevmajor)
        if request.form.get("IELTS[R]") is not None:
            LELTSmoreR = request.form.get("IELTS[R]",0,int)
            LELTSmoreL = request.form.get("IELTS[L]")
            LELTSmoreS = request.form.get("IELTS[S]")
            LELTSmoreW = request.form.get("IELTS[W]")

            if request.form.get("GRE[V]") is not None:
                GREmoreV = request.form.get("GRE[V]")
                GREmoreQ = request.form.get("GRE[Q]")
                GREmoreAW = request.form.get("GRE[AW]")
                Score.set_user_info(connection=g.db,user_id=user_id,
                                    IELTS_r=LELTSmoreR,
                                    IELTS_l=LELTSmoreL,
                                    IELTS_s=LELTSmoreS,
                                    IELTS_w=LELTSmoreW,
                                    GRE_v=GREmoreV,
                                    GRE_q=GREmoreQ,
                                    GRE_aw=GREmoreAW

                                    )
            else:
                GMATmoreV = request.form.get("GMAT[V]")
                GMATmoreQ = request.form.get("GMAT[Q]")
                GMATmoreAW = request.form.get("GMAT[AW]")
                GMATmoreIR = request.form.get("GMAT[IR]")
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
            TOEFLmoreR = request.form.get("TOEFL[R]")
            TOEFLmoreL = request.form.get("TOEFL[L]")
            TOEFLmoreS = request.form.get("TOEFL[S]")
            TOEFLmoreW = request.form.get("TOEFL[W]")

            if request.form.get("GRE[V]") is not None:
                GREmoreV = request.form.get("GRE[V]")
                GREmoreQ = request.form.get("GRE[Q]")
                GREmoreAW = request.form.get("GRE[AW]")
                Score.set_user_info(connection=g.db,user_id=user_id,
                                    TOEFL_r =TOEFLmoreR,
                                    TOEFL_l =TOEFLmoreL,
                                    TOEFL_s =TOEFLmoreS,
                                    TOEFL_w =TOEFLmoreW,
                                    GRE_v=GREmoreV,
                                    GRE_q=GREmoreQ,
                                    GRE_aw=GREmoreAW

                                    )
            else:
                GMATmoreV = request.form.get("GMAT[V]")
                GMATmoreQ = request.form.get("GMAT[Q]")
                GMATmoreAW = request.form.get("GMAT[AW]")
                GMATmoreIR = request.form.get("GMAT[IR]")
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




