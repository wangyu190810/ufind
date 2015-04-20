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
    version = "v1",
    yunpian = {
        "host":"yunpian.com",
        # 端口号
        "port":80,
        # 版本号

        # 查账户信息的URI
        "user_get_uri":"/" + version + "/user/get.json",
        # 通用短信接口的URI
        "sms_send_uri":"/" + version + "/sms/send.json",
        # 模板短信接口的URI
        "sms_tpl_send_uri":"/" + version + "/sms/tpl_send.json"
    }