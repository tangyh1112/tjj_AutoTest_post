#!C:\Users\dell\AppData\Local\Programs\Python\Python35 python
# -*- coding: utf-8 -*-

def cookie(cj):
    dict_cookie = {}
    dict_cookie.update({'Cookie': "x-cc-user=null; x-cc-user-token=" + cj['x-cc-user-token'] + "; AUTH_TOKEN_SAVE="
                "" + cj['AUTH_TOKEN_SAVE'] + ";USER_ID=" + cj['USER_ID'] + "; AUTH_TOKEN_SAVE_KEY=" + cj[
                'AUTH_TOKEN_SAVE_KEY'] + "; VALID_TIME=" + cj['VALID_TIME'] + "; USER_TYPE_ID=" + cj[
                'USER_TYPE_ID'] + ""})
    return dict_cookie['Cookie']
