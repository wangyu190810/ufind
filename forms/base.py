# coding: utf-8
# email: khahux@163.com

import re

from flask_wtf import Form


RE_EMAIL = re.compile(r'^.+@[^.].*\.[a-z]{2,10}$')


class BaseForm(Form):
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
