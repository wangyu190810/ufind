# coding: utf-8
# email: khahux@163.com

from wtforms import StringField, validators

from .base import BaseForm


EMPTY = 'Can not be empty.'


class LoginForm(BaseForm):
    username = StringField('username', [
        validators.DataRequired(message=EMPTY)
    ])
    password = StringField('password', [
        validators.DataRequired(message=EMPTY)
    ])