__author__ = 'wangyu'
from flask import Flask, g, current_app
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from datetime import timedelta

from mysite.view.university import get_university, get_search_university, \
    get_university_info, get_university_list, get_state_university
from mysite.view.major import search_major, get_major_compare,\
    get_major_from_university_faculty
from mysite.view.user import get_user_info, get_user_detail_info, \
    get_user_in_university, update_user_bginf, get_user_base_info,\
    edit_user_info_page, update_user_info,update_user_description
from mysite.view.score import set_user_score
from mysite.view.compare import set_compare, get_compare, get_compare_list, \
    set_compare_support
from mysite.view.offer import set_offer, get_offer_student
from mysite.view.login import login, logout, register_first, register_second,\
    change_password,login_from_cookie
from mysite.view.message import set_message, get_message,set_message_to_gov,\
    del_message_to_user
from mysite.view.state import get_index
from mysite.view.sms import send_sms
from mysite.view.china_school import search_major_name, search_university_china
from mysite.view.user_follow import del_follow_user, set_follow_user
from mysite.view.sub import get_sub
from mysite.view.uploadhead import upload_file,get_random_head

from mysite.mobile.view import mobile_send_sms

from config import Config


app = Flask(__name__)
app.secret_key = Config.SUCCESS_KEY
app.permanent_session_lifetime = timedelta(minutes=60*24)
app.config["SQLALCHEMY_DATABASE_URI"] = Config.db


app.sa_engine = create_engine(Config.db)
app.DBSession = scoped_session(sessionmaker(bind=app.sa_engine))


app.add_url_rule("/api/login", view_func=login,
                 methods=["GET", "POST"])
app.add_url_rule("/api/login_cookie",view_func=login_from_cookie,
                 methods=["GET"])
app.add_url_rule("/api/logout", view_func=logout,
                 methods=["GET", "POST"])

app.add_url_rule("/api/get_university",
                 view_func=get_university, methods=["GET"])
app.add_url_rule("/api/search_university",
                 view_func=get_search_university, methods=["GET"])
app.add_url_rule("/api/search_major",
                 view_func=search_major, methods=["GET"])
app.add_url_rule("/api/university_info",
                 view_func=get_university_info, methods=["GET"])
app.add_url_rule("/api/student_info",
                 view_func=get_user_info, methods=["GET"])
app.add_url_rule("/api/get_user_detail_info",
                 view_func=get_user_detail_info, methods=["GET"])
app.add_url_rule("/api/get_user_in_university", methods=["POST"],
                 view_func=get_user_in_university)
#app.add_url_rule("/api/set_user_score", view_func=set_user_score,
#                 methods=["POST"])
app.add_url_rule("/api/set_compare", view_func=set_compare,
                 methods=["POST"])
app.add_url_rule("/api/set_compare_support", methods=["POST"],
                 view_func=set_compare_support)


app.add_url_rule("/api/set_offer", view_func=set_offer,
                 methods=["POST"])
app.add_url_rule("/api/get_sub",view_func=get_sub,
                 methods=["GET"])
app.add_url_rule("/api/set_user_score",view_func=set_user_score,
                 methods=["POST"])

app.add_url_rule("/api/update_user_bginf", view_func=update_user_bginf,
                 methods=["POST"])
app.add_url_rule("/api/update_user_description",view_func=update_user_description,
                 methods=["POST"])
app.add_url_rule("/api/get_user_base_info", view_func=get_user_base_info,
                 methods=["GET"])
app.add_url_rule("/api/edit_user_info_page", view_func=edit_user_info_page,
                 methods=["GET"])
app.add_url_rule("/api/update_user_info", view_func=update_user_info,
                 methods=["POST"])
app.add_url_rule("/api/get_compare", view_func=get_compare,
                 methods=["GET"])
app.add_url_rule("/api/get_major_compare", view_func=get_major_compare,
                 methods=["GET"])
app.add_url_rule("/api/get_compare_list", view_func=get_compare_list,
                 methods=["POST"])
app.add_url_rule("/api/get_offer_student_id", view_func=get_offer_student,
                 methods=["GET"])
app.add_url_rule("/api/university_list", view_func=get_university_list,
                 methods=["GET"])
app.add_url_rule("/api/get_major_form_university_faculty", methods=["GET"],
                 view_func=get_major_from_university_faculty)

app.add_url_rule("/api/set_message", view_func=set_message,
                 methods=["POST"])
app.add_url_rule("/api/get_message", view_func=get_message,
                 methods=["GET"])
app.add_url_rule("/api/send_advice",view_func=set_message_to_gov,
                 methods=["POST"])
app.add_url_rule("/api/del_message_to_user",view_func=del_message_to_user,
                 methods=["POST"])


app.add_url_rule("/api/get_state_university", view_func=get_state_university,
                 methods=["GET"])
app.add_url_rule("/api/index", view_func=get_index,
                 methods=["GET"])
app.add_url_rule("/api/register_first", view_func=register_first,
                 methods=["POST"])
app.add_url_rule("/api/register_second", view_func=register_second,
                 methods=["POST"])
app.add_url_rule("/api/change_password", view_func=change_password,
                 methods=["POST"])
app.add_url_rule("/api/send_sms", view_func=send_sms,
                 methods=["POST"])
# app.add_url_rule("/googlefad2f2add41d5dac.html",

# view_func=google)

app.add_url_rule("/api/set_follow_user",methods=["POST"],
                 view_func=set_follow_user)
app.add_url_rule("/api/del_follow_user",methods=["POST"],
                 view_func=del_follow_user)


app.add_url_rule("/api/search_university_china",methods=["GET"],
                 view_func=search_university_china)
app.add_url_rule("/api/search_major_china",methods=["GET"],
                 view_func=search_major_name)


app.add_url_rule("/api/upload_headimg",view_func=upload_file,
                 methods=["GET", "POST"])
app.add_url_rule("/api/get_random_head",view_func=get_random_head,
                 methods=["GET"])


# 移动端api
app.add_url_rule("/api/mobile/send_sms",view_func=mobile_send_sms,
                 methods=["POST"])


@app.before_request
def _before_request():
    g.db = current_app.DBSession()


@app.teardown_request
def teardown_request(*a, **k):
    current_app.DBSession.remove()
    g.db.close()
