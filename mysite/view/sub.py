# -*-coding: utf-8-*-

__author__ = 'wangyu'

from flask import g,jsonify,request

from mysite.model.stasub import SubContent


def get_sub():
    if request.method == "GET":
        sub_type = request.args.get("sub_type")
        sub_list = list()
        for row in SubContent.get_sub_content(g.db,int(sub_type)):
            sub_dict = dict()
            sub_dict["id"] = row.id
            sub_dict["name"] = row.content
            sub_list.append(sub_dict)

        return jsonify(sublist=sub_list,
                       status="success")


