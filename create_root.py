# -*-coding: utf-8-*-

__author__ = 'wangyu'

from mysite.model.user import User
from mysite.application import app


def root():
    username = raw_input("username")
    password = raw_input("password")
    user = User(username=username,password=password)
    app.DBSession.add(user)
    app.DBSession.commit()


if __name__ == '__main__':
    root()

