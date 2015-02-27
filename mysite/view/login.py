__author__ = 'wangyu'
from flask import render_template,redirect,g,session,request,jsonify
from mysite.view.base import allow_cross_domain
from mysite.model.user import User

import json

@allow_cross_domain
def login():
#    if request.method == "GET":
#        return render_template("login.html")

    email, password = map(request.form.get,("email","password"))
    user = User.login_user(g.db,email,password)
    if user.id is not None:
        session["user_id"] = user.id
        student = {}
        student["studentid"] = user.id
        student["studentname"] = user.username
        student["studentpic"] = user.pic
        return jsonify(status="success",
                       student=student
                       )
    return jsonify(status="false")

@allow_cross_domain
def register_first():
    if request.method == "POST":
        print request.data
        data = json.loads(request.data)
        print data
        email  = data["email"]
        passwrod = data["password"]
        phonenum = data["phonenum"]
        checknum = data["checknum"]
        check = User.get_checknum(g.db,phonenum)
        if check is None:
            print "12"
            return jsonify(status="false")
        elif check == int(checknum):
            User.register_first(g.db,email,passwrod,phonenum)
            return jsonify(status="success")
        else:
            return jsonify(status="false")


@allow_cross_domain
def logout():
    session.pop("username")
    return redirect("/index")



