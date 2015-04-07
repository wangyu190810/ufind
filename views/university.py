# coding: utf-8
# email: khahux@163.com

import json

from flask import request, jsonify, g

from models.offer import Offer
from models.major import Major
from models.state import State
from models.faculty import Faculty
from models.university import University

from lib.decorators import allow_cross_domain
from lib.get_static import get_university_img, get_university_logo, get_university_state, get_main_major


@allow_cross_domain
def get_university():
    if request.method == "GET":
        university_id = request.args.get("universityid")
        university = {}
        faculty = {}
        if university_id == 0:
            for university in University.get_university_info(connection=g.db):
                c = university.__dict__
                return jsonify(data=json.dumps(c), status=u"success")
        else:
            university_info = []
            faculty_info = []
            for row in University.get_university_info(g.db, university_id):
                university["name"] = row.name
                university["chiname"] = row.chiname
                university["universitypic"] = get_university_img(row.name, 2, u"地图长方形图片")
                university_info.append(university)

            for row in Faculty.get_faculty_info(g.db, university_id):
                faculty["name"] = row.name
                faculty["chiname"] = row.chiname
                faculty["facultyid"] = row.id
                faculty_info.append(faculty)
                faculty = {}

            return jsonify(universityinfo=university_info,
                           faculty=faculty_info,
                           status="success")


#@allow_cross_domain
def get_university_info():
    if request.method == "GET":
        university_id = request.args.get("universityid")
        university_info = {}
        facultylist = []
        faculty = {}
        majorlist = []
        major = {}
        link = {}
        for row in University.get_university_info(g.db, university_id):
            university_info["universityid"] = row.id
            university_info["universitylogo"] = get_university_logo(row.name)
            link["baidu"] = row.baidu
            link["wiki"] = row.wiki
            link["official"] = row.official
            university_info["name"] = row.name
            university_info["chiname"] = row.chiname
            university_info["offernum"] = Offer.get_offer_num(g.db, row.id)
            university_info["pic1"] = get_university_img(row.name, 1, u"长方形图片")
            university_info["pic2"] = get_university_img(row.name, 2, u"长方形图片")
            university_info["link"] = link
        for row in Faculty.get_faculty_info(g.db, university_id):
            faculty["facultyid"] = row.id
            faculty["chiname"] = row.chiname
            faculty["name"] = row.name
            # faculty["pic"] = get_main_major(1,row.main_major)
            num = 1
            for major_row in Major.get_major_info(g.db,
                                                  university_info["universityid"],
                                                  faculty["facultyid"]):
                major["majorid"] = major_row.id
                major["name"] = major_row.name
                img_num = 2
                if num % 3:
                    img_num = 1
                print img_num
                print num

                check = 1
                major["pic"] = get_main_major(img_num,major_row.main_major)
               # major["pic2"] = get_main_major(2,major_row.main_major)
                for major_check in majorlist:
                    if major["name"] in major_check.get("name"):
                        check = 0
                        print "123414"
                        break

                if check:
                    majorlist.append(major)

                major = {}

                num += 1
                if num == 4:
                    break

            faculty["majorlist"] = majorlist
            majorlist = []
            facultylist.append(faculty)
            faculty = {}
        university_info["facultylist"] = facultylist
        university_info["status"] = "success"
        return json.dumps(university_info)


@allow_cross_domain
def get_search_university():
    if request.method == "GET":
        searchname, stateid = map(request.args.get, ("searchname", "stateid"))
        universitylist = []
        university = {}
        if stateid is None:

            for row in University.search_university(g.db, searchname):
                university["name"] = row.name
                university["chiname"] = row.chiname
                university["id"] = row.id
                university["logo"] = get_university_logo(row.name)
                universitylist.append(university)
                university = {}
            return jsonify(namelist=universitylist,
                           stattus="success")
        else:
            for row in University.search_university(g.db, searchname, stateid):
                university["name"] = row.name
                university["chiname"] = row.chiname
                university["id"] = row.id
                university["logo"] = get_university_logo(row.name)
                universitylist.append(university)
                university = {}
            return jsonify(namelist=universitylist,
                           stattus="success")


@allow_cross_domain
def get_university_list():
    if request.method == "GET":
        name = []
        for row in University.university_name_list(g.db):
            name.append(row.name)
        return jsonify(university=name)


# @allow_cross_domain
def get_state_university():
    if request.method == "GET":
        university = {}
        state_id = request.args.get("stateid")
        university["statepic"] = get_university_state(
            State.get_state_name(g.db, state_id).name)
        universitylist = []
        university_info = {}
        for row in University.get_state_university(g.db, state_id):
            university_info["name"] = row.name
            university_info["chiname"] = row.chiname
            university_info["universityid"] = row.id
            university_info["universitypic"] = get_university_img(row.name, 2, u"方形图片")
            university_info["latitude"] = row.latitude
            university_info["longitude"] = row.longitude
            university_info["offernum"] = Offer.get_offer_num(g.db, row.id)
            university_info["meanGPA"] = "32"
            university_info["meanTOEFL"] = "123"
            universitylist.append(university_info)
            university_info = {}
        university["universitylist"] = universitylist
        university["status"] = "success"
        return json.dumps(university)