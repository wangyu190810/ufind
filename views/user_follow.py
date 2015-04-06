# coding: utf-8
# email: khahux@163.com

from flask import g, jsonify, request, session

from models.user import UserFollow
from lib.decorators import allow_cross_domain


@allow_cross_domain
def set_follow_user():
    """"""
    if request.method == "POST":
        user_id = session.get("user_id")
        follow_user_id = request.form.get("follow_user_id")
        UserFollow.set_follow(g.db, user_id, follow_user_id)
        return jsonify(status="success")
    return jsonify(status="false")


@allow_cross_domain
def del_follow_user():
    if request.method == "POST":
        user_id = session.get("user_id")
        follow_user_id = request.form.get("follow_user_id")
        UserFollow.del_follow_id(g.db, user_id, follow_user_id)
        return jsonify(status="success")
    return jsonify(status="false")