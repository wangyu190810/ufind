# -*-coding: utf-8-*-

__author__ = 'wangyu'

import json
from random import randint

from flask import request,g

from mysite.view.base import allow_cross_domain
from mysite.model.state import State
from mysite.model.offer import Offer


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
            #state["offernum"] = row.offernum
            state["offernum"] = randint(100, 300)
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
        data["offernum"] = Offer.get_site_offer_num(g.db)
        data["status"] = "success"
        return json.dumps(data)