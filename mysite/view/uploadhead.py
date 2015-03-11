# -*-coding:utf-8-*-
__author__ = 'Administrator'
from flask import g, jsonify,request,redirect
from werkzeug import secure_filename
import os
from config import Config


def allowed_file(filename):
    return "." in filename and \
           filename.rsplit(".", 1)[1] in Config.allowed_extensions


def upload_file():
    if request.method == "POST":
        head = request.files["head"]
        print head
        if head and allowed_file(head.filename):
            filename = secure_filename(head.filename)
            print filename
            head.save(os.path.join(Config.upload_folder, filename))
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
