# coding: utf-8
# email: khahux@163.com

from datetime import timedelta

from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from config import Config


def ufindoffer_app():
    app = Flask(__name__)
    app.secret_key = Config.SUCCESS_KEY
    app.permanent_session_lifetime = timedelta(minutes=60*24)
    app.config["SQLALCHEMY_DATABASE_URI"] = Config.db

    app.sa_engine = create_engine(Config.db)
    app.DBSession = scoped_session(sessionmaker(bind=app.sa_engine))

    return app

