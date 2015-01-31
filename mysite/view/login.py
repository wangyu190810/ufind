__author__ = 'wangyu'
from flask import render_template,redirect,g,session,request,jsonify

from mysite.model.user import User


def login():
    if request.method == "GET":
        return render_template("login.html")

    phone, password = map(request.form.get,("phone","password"))
    print (phone,password)
    user_id = User.login_user(g.db,phone,password)
    for row in user_id:
        print row
        if row[0] is not None:
            session["user_id"] = row[0]
            return jsonify(status="success")
        return redirect("/index")


def logout():
    session.pop("username")
    return redirect("/index")



