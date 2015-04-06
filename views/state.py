# coding: utf-8
# email: khahux@163.com

import json
from random import randint

from flask import request, g

from models.state import State
from models.offer import Offer

from lib.decorators import allow_cross_domain


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
        for row in State.get_index(g.db, "USA"):
            state["stateid"] = row.id
            state["name"] = row.name
            state["latitude"] = row.latitude
            state["longitude"] = row.longitude
            # state["offernum"] = row.offernum
            state["offernum"] = randint(100, 300)
            country.append(state)
            state = {}
        local["USA"] = country
        country = []
        for row in State.get_index(g.db, "UK"):
            state["stateid"] = row.id
            state["name"] = row.name
            state["latitude"] = row.latitude
            state["longitude"] = row.longitude
            state["offernum"] = row.offernum
            country.append(state)
            state = {}
        local["UK"] = country
        country = []
        for row in State.get_index(g.db, "AUS"):
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
        data["offernum"] = Offer.get_site_offer_num(g.db)
        data["status"] = "success"
        return json.dumps(data)