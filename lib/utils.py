# coding: utf-8
# email: khahux@163.com

import time
from itsdangerous import Signer

from config import Config


def get_timestamp(create_time):
    timeArray = time.localtime(create_time)
    return time.strftime("%Y-%m-%d %H:%M:%S", timeArray)


def get_Total(r, l, s, w):
    return r+l+s+w


def get_TELTS(r, l, s, w):
    score = float(r+l+s+w)/4
    if int((score * 10) / 10) == score:
        return score
    elif (score * 10) % 5 == 0:
        return score
    elif (score * 10) % 5 < 5:
        return int(score)
    elif (score * 10) % 5 > 5:
        return int(score)+1


def get_gre(v, q):
    return v+q


def get_GMAT(v, q):
    return v + q


def get_SAT(CR, M, W):
    return CR + M + W


def get_compare_score(GPA_TO, GPA_from, GPA):
    # if GPA_TO > GPA and GPA_from < GPA:
    if float(GPA_from) <= float(GPA) and float(GPA_TO) >= float(GPA):
        return True
    elif float(GPA_from) >= float(GPA) and float(GPA_TO) <= float(GPA):
        return True
    return False


def set_sign_safe(sign_file):
    s = Signer(Config.login_sign)
    return s.sign(sign_file)


def get_sign_safe(true_file):
    s = Signer(Config.login_sign)
    return s.unsign(true_file)


def checknum_timeout(sms_time):
    if ((time.time() - sms_time) / 60) > 30:
        return False
    return True