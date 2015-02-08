#!-*-coding:utf-8-*-
__author__ = 'wangyu'
from flask import render_template,request,g,redirect,jsonify,session
import json
from mysite.model.blog import Blog
from mysite.model.message import Message
from mysite.model.user import User
from mysite.view.base import validate_user_login


def get_message():
    if request.method == "GET":
        user_id = request.args.get("user_id")
        messagelist = []
        message = {}
        user_message = {}
        for row in Message.get_message(g.db,user_id):
            user_message["message_user_id"] = row.message_user_id
            #user_message["message_user_name"] = row.message_user_name
            print User.get_user_name(g.db,user_id).id

            user_message["message_user_name"] = User.get_user_name(g.db,user_id).username
            user_message["message"] = row.message
            messagelist.append(user_message)
            user_message = {}

        message["message"] = messagelist
        print(message)
        return json.dumps(message)


def set_message():
    if request.method == "POST":
        user_id = session["user_id"]
        data = json.loads(request.data)
        print data
        message_user_id = data["message_user_id"]

        message = data["message"]
        print(message_user_id,message)
        Message.set_message(g.db,user_id,message_user_id,message)
        return jsonify(status="success")