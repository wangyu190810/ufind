# coding: utf-8
# email: khahux@163.com

import json

from flask import request, g, jsonify, session

from models.user import User
from models.message import Message

from lib.utils import get_timestamp
from lib.decorators import validate_user_login, allow_cross_domain


@allow_cross_domain
@validate_user_login
def get_message():
    if request.method == "GET":
        message_user_id = request.args.get("user_id")
        messagelist = list()
        message = dict()
        for row in Message.get_message_user(g.db, message_user_id):
            user_message = dict()
            user_message["studentid"] = row.user_id
            user_message["messageid"] = row.id
            user_message["time"] = get_timestamp(row.create_time)
            user = User.get_user_name(g.db, row.user_id)
            user_message["name"] = user.username
            user_message["pic"] = user.pic
            user_message["content"] = row.message

            messagelist.append(user_message)

        message["messages"] = messagelist
        return json.dumps(message)
    return jsonify(status="false")


@allow_cross_domain
@validate_user_login
def set_message():
    if request.method == "POST":
        user_id = session.get("user_id")
        message = request.form.get("message")
        message_user_id = request.form.get("message_user_id")
        Message.set_message(g.db, user_id, message_user_id, message)
        return jsonify(status="success")
    return jsonify(status="false")


@allow_cross_domain
@validate_user_login
def set_message_to_gov():
    if request.method == "POST":
        user_id = session.get("user_id")
        data = request.form
        message = data["content"]
        Message.set_message_to_gov(g.db, user_id, message)
        return jsonify(status="success")
    return jsonify(status="false")


@allow_cross_domain
@validate_user_login
def del_message_to_user():
    if request.method == "POST":
        data = request.form
        user_id = session.get("user_id")
        message_id = data["message_id"]
        message = Message.get_message_info(g.db, message_id)
        if message.message_user_id == int(user_id):
            Message.del_message_to_user(g.db, message_id)
            return jsonify(status="success")
        return jsonify(status="codeerror")
    return jsonify(status="false")
