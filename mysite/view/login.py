__author__ = 'wangyu'
from flask import render_template,redirect,g,session,request,jsonify
from mysite.view.base import allow_cross_domain
from mysite.model.user import User

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

    return jsonify(status="falue")
@allow_cross_domain
def register():
    if request.method == "POST":
        pass


@allow_cross_domain
def logout():
    session.pop("username")
    return redirect("/index")



