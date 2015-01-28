#! /usr/bin/python
#-*- coding:utf-8 -*-
#Filename: university.py
#Author: wangyu190810
#E-mail: wo190810401@gmail.com
#Date: 2015-01-22
#Description: 

import json
from mysite.model.university import University
from mysite.model.faculty import Faculty
from mysite.model.major import Major
from mysite.model.offer import Offer
from flask import request,jsonify,g


def set_offer():
    if request.method == "POST":

        data = request.data
        data = json.loads(data)
        offer = data["offers"]
        user_id = 12312
        for row in offer:
            university_id = int(row["universityid"])
            major_id = int(row["majorid"])
            result = int(row["result"])
            Offer.set_offer(g.db,
                            user_id=user_id,
                            university_id=university_id,
                            major_id=major_id,
                            result=result)

        return jsonify(status="success",
                       img="asdfsda")

