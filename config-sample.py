#-*-coding:utf-8-*-
__author__ = 'wangyu'

class Config(object):
    db = "mysql://root:1234@localhost/ufind?charset=utf8"
    SUCCESS_KEY = "@åßßßßßå∂åß∂œ∑œ∑œ∑œ∑œœ∑åßåß∂åß∂ΩΩΩ≈çΩ≈ç"
    REDIS_URL = "redis:://:"
    apikey = ""
    login_sign = u"随意的签名"
    upload_folder = "."
    allowed_extensions = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
    salt = u"加盐加盐"