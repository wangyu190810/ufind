__author__ = 'wangyu'
from flask import Flask, g, current_app
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from datetime import timedelta

from mysite.view.university import get_university, get_search_university, \
    get_university_info
from mysite.view.major import search_major
from mysite.view.user import get_user_info
from mysite.view.score import set_user_info
from mysite.view.compare import set_compare, get_compare
from mysite.view.offer import set_offer
from config import Config


app = Flask(__name__)
app.secret_key = Config.SUCCESS_KEY
app.permanent_session_lifetime = timedelta(minutes=60)
app.config["SQLALCHEMY_DATABASE_URI"] = Config.db

app.sa_engine = create_engine(Config.db)
app.DBSession = scoped_session(sessionmaker(bind=app.sa_engine))
#
# app.add_url_rule("/",view_func=index,methods=["GET", "POST"])
# app.add_url_rule("/edit",view_func=edit,methods=["GET", "POST"])
# app.add_url_rule("/change/<int:blog_id>",view_func=blog_change,methods=["GET","POST"])
# app.add_url_rule("/search",view_func=search,methods=["GET"])
#
# app.add_url_rule("/arch",view_func=arch,methods=["GET"])
# app.add_url_rule("/blog/<int:blog_id>",view_func=blog,methods=["GET","POST"])
# app.add_url_rule("/tag/<tag>",view_func=blog_tag,methods=["GET","POST"])
# app.add_url_rule("/classify/<name>",view_func=blog_classify,methods=["GET","POST"])
#
#
# app.add_url_rule("/login",view_func=login,methods=["GET","POST"])
# app.add_url_rule("/logout",view_func=logout,methods=["GET","POST"])

app.add_url_rule("/api/get_university",
                 view_func=get_university, methods=["GET"])
app.add_url_rule("/api/search_university",
                 view_func=get_search_university, methods=["GET"])
app.add_url_rule("/api/search_major",
                 view_func=search_major, methods=["GET"])
app.add_url_rule("/api/university_info",
                 view_func=get_university_info, methods=["GET"])
app.add_url_rule("/api/student_info/<int:studentid>",
                 view_func=get_user_info, methods=["GET"])
app.add_url_rule("/api/set_user_info", view_func=set_user_info,
                 methods=["POST"])
app.add_url_rule("/api/set_compare", view_func=set_compare,
                 methods=["POST"])
app.add_url_rule("/api/set_offer", view_func=set_offer,
                 methods=["POST"])
app.add_url_rule("/api/get_compare", view_func=get_compare,
                 methods=["GET"])
# app.add_url_rule("/googlefad2f2add41d5dac.html",
# view_func=google)


@app.before_request
def _before_request():
    g.db = current_app.DBSession()


@app.teardown_request
def teardown_request(*a, **k):
    current_app.DBSession.remove()
    g.db.close()
