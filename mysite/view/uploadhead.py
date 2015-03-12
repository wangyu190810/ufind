# -*-coding:utf-8-*-
__author__ = 'Administrator'
from flask import g, jsonify,request,redirect,session
from werkzeug import secure_filename
import os

from config import Config
from mysite.view.base import validate_user_login,get_user_hred_img
from mysite.view.user import User
import random

def allowed_file(filename):
    return "." in filename and \
           filename.rsplit(".", 1)[1] in Config.allowed_extensions

@validate_user_login
def upload_file():
    if request.method == "POST":
        user_id = session.get("user_id")
        head = request.files["head"]
        print head
        if head and allowed_file(head.filename):
            filename = secure_filename(head.filename)
            print filename
            head.save(os.path.join(Config.upload_folder, filename))
            link = "http://www.ufindoffer.com/images/medivh/"+filename
            User.update_user_pic(g.db, user_id, link)
            return jsonify(status="success")
            #return jsonify(status="success")
    return """ <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=POST enctype=multipart/form-data>
      <p><input type=file name=head>
         <input type=submit value=Upload>
    </form>
    """

@validate_user_login
def get_random_head():
    if request.method == "GET":
        head_list = list()
        for row in range(1, 18):
            girl = get_user_hred_img(u"无性别",row)
            boy = get_user_hred_img(u"男生",row)
            #if girl not in head_list:
            head_list.append(girl)
            #if boy not in head_list:
            head_list.append(boy)
        for row in range(1,40):
            nosex = get_user_hred_img(u"女生",row)
            head_list.append(nosex)
        random.shuffle(head_list)
        return jsonify(status="success",
                       imageslist=head_list)
    return jsonify(status="false")

