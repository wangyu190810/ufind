# coding: utf-8
# email: khahux@163.com


def get_university_img(universityname, num, shape):
    return u"http://www.ufindoffer.com/images/unimg/all_un/"+universityname+u"/"+shape+u"/"+unicode(num)+".jpg"


def get_university_logo(universityname):
    return u"http://www.ufindoffer.com/images/unimg/all_logo/"+universityname+".png"


def get_university_state(statename):
    return u"http://www.ufindoffer.com/images/unimg/state/"+statename+".jpg"


def get_user_hred_img(sex, max_num):
    return u"http://www.ufindoffer.com/images/unimg/head/"+unicode(sex)+"/"+unicode(max_num)+".jpg"


def get_university_twodim(universityname):
    return u"http://www.ufindoffer.com/images/unimg/twodim/"+universityname+".jpg"


def get_main_major(num, name):
    return u"http://www.ufindoffer.com/images/unimg/major/"+name+str(num)+".png"