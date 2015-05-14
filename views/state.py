# coding: utf-8
# email: khahux@163.com

import json
from random import randint


from flask import request, g, session
from lib.decorators import allow_cross_domain,login_user_info
from models.state import State
from models.offer import Offer
from models.user import User



@allow_cross_domain
def get_state_info():
    if request.method == "GET":
        country = []
        state = {}
        for row in State.get_state_info(g.db):
            state["stateid"] = row.id
            state["name"] = row.name
            state["offernum"] = row.offernum
            country.append(state)
            state = {}


@allow_cross_domain
def get_index():
    if request.method == "GET":
        statelist = {}
        country = []
        state = {}
        local = {}
        data = {}
        user_type = None
        user = User.get_user_info(g.db,user_id=session.get("user_id"))
        if user:
            user_type = user.type



        for row in State.get_index(g.db,u"USA"):

            state["stateid"] = row.id
            state["name"] = row.name
            state["latitude"] = row.latitude
            state["longitude"] = row.longitude
            if user_type is None:
                state["offernum"] = row.offernum
            elif user_type == 0:
                state["offernum"] = row.offernum_0
            else:
                state["offernum"] = row.offernum_1

            country.append(state)
            state = {}
        local["USA"] = country
        country = []
        for row in State.get_index(g.db,u"UK"):
            state["stateid"] = row.id
            state["name"] = row.name
            state["latitude"] = row.latitude
            state["longitude"] = row.longitude
            if user_type is None:
                state["offernum"] = row.offernum
            elif user_type == 0:
                state["offernum"] = row.offernum_0
            else:
                state["offernum"] = row.offernum_1
            country.append(state)
            state = {}
        local["UK"] = country
        country = []
        for row in State.get_index(g.db,u"AUS"):

            state["stateid"] = row.id
            state["name"] = row.name
            state["latitude"] = row.latitude
            state["longitude"] = row.longitude
            if user_type is None:
                state["offernum"] = row.offernum
            elif user_type == 0:
                state["offernum"] = row.offernum_0
            else:
                state["offernum"] = row.offernum_1
            country.append(state)
            state = {}
        local["AUS"] = country
        statelist["USA"] = local["USA"]
        statelist["UK"] = local["UK"]
        statelist["AUS"] = local["AUS"]
        data["statelist"] = statelist
        data["offernum"] = Offer.get_site_offer_num(g.db, user_type) + 500
        data["status"] = "success"
        return json.dumps(data)