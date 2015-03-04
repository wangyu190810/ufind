#! /usr/bin/python
# -*- coding:utf-8 -*-
# Filename: university.py
# Author: wangyu190810
# E-mail: wo190810401@gmail.com
# Date: 2015-01-22
# Description:

import json
from flask import request,g
from mysite.view.base import allow_cross_domain,login_user_info
from mysite.model.state import State

@allow_cross_domain
def get_state_info():
    if request.method == "GET":
        statelist = {}
        country = []
        state = {}
        for row in State.get_state_info(g.db):
            state["stateid"] = row.id
            state["name"] = row.name
            state["offernum"] = row.offernum
            country.append(state)
            state = {}

#@login_user_info
@allow_cross_domain
def get_index():
    if request.method == "GET":
        statelist = {}
        country = []
        state = {}
        local = {}
        data = {}
        for row in State.get_index(g.db,"USA"):
            state["stateid"] = row.id
            state["name"] = row.name
            state["latitude"] = row.latitude
            state["longitude"] = row.longitude
            state["offernum"] = row.offernum
            country.append(state)
            state = {}
        local["USA"] = country
        country = []
        for row in State.get_index(g.db,"UK"):
            state["stateid"] = row.id
            state["name"] = row.name
            state["latitude"] = row.latitude
            state["longitude"] = row.longitude
            state["offernum"] = row.offernum
            country.append(state)
            state = {}
        local["UK"] = country
        country = []
        for row in State.get_index(g.db,"AUS"):
            state["stateid"] = row.id
            state["name"] = row.name
            state["latitude"] = row.latitude
            state["longitude"] = row.longitude
            state["offernum"] = row.offernum
            country.append(state)
            state = {}
        local["AUS"] = country
        statelist["USA"] = local["USA"]
        statelist["UK"] = local["UK"]
        statelist["AUS"] = local["AUS"]
        data["statelist"] = statelist
        data["offernum"] = "123"
        data["status"] = "success"
        return json.dumps(data)