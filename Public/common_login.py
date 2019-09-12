#!C:\Users\dell\AppData\Local\Programs\Python\Python35 python
# -*- coding: utf-8 -*-
import requests
import json
import readConfig as readConfig
import logging
from Public.Utils import utils
import os
import http.cookiejar
import urllib.request,urllib.parse, urllib.error
localReadConfig = readConfig.ReadConfig()

class Login:
    def __init__(self):
        self.hostsit = localReadConfig.get_http("baseurlsit")
        self.timeout = localReadConfig.get_http("timeout")

    def post_login(self, login_params, params):
        login_dic = {}
        try:
            headers = json.loads(login_params['login']['headers'])
            # params = login_params['login']['params']
            url = 'http://sit.317hu.com/care-nurse/nurse/account/login/byPassword'#self.hostsit + login_params['login']['url']
            response = requests.post(url, params=params, headers=headers, timeout=float(self.timeout))
            response.raise_for_status()
            login_dic.update({'token': response.headers.get('token')})
            login_dic.update({'submittoken': response.headers.get('submittoken')})
            login_dic.update({'devicenumber': response.headers.get('devicenumber')})
            login_response = json.loads(response.text)
            login_dic.update({'accountid': login_response['data']['id']})
            login_dic.update({'hospitalId': login_response['data']['hospital']['id']})
            login_dic.update({'accountName': login_response['data']['login']})
            login_dic.update({'name': login_response['data']['name']})
            login_dic.update({'hospitalName': login_response['data']['dept']['hospitalName']})
            if login_response['data']['wardList'][0]:
                login_dic.update({'wardId': login_response['data']['wardList'][0]['id']})# 20180521 新增获取wardId
            logging.info('调用登录接口获取用户信息成功')
            # logging.info(login_dic)
            return login_dic
        except TimeoutError as e:

            logging.error(e)
            raise Exception(e)

class Login_web:
    def __init__(self):
        self.hostsit = localReadConfig.get_http("baseurlsit")
        self.timeout = localReadConfig.get_http("timeout")
        self.hostsit_admin = localReadConfig.get_http("bizcenterWeb")
        self.hostsit_document = localReadConfig.get_http("documentConverUrl")
    def post_login_web(self, login_params_web,params,filename,case_path):
        try:
            headers = {
                'content-type': "application/x-www-form-urlencoded",
                'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
            }
            postdata = urllib.parse.urlencode(params).encode(encoding='UTF8')
            #url = "http://ucsit.317hu.com:8082/userCentral-web/user/accountRest/login"
            url = "http://usercentral-sit.317hu.com/userCentral-web/user/accountRest/login"
            cookiefile = os.path.join(case_path, filename)
            cookie = http.cookiejar.LWPCookieJar(cookiefile)
            handler = urllib.request.HTTPCookieProcessor(cookie)
            opener = urllib.request.build_opener(handler)
            response = urllib.request.Request(url, data=postdata, headers=headers)
            print("response = %s" %response)
            try:
                opener.open(response)
            except urllib.error.URLError as e:
                print(e.code, ':', e.reason)
            cookie.save(ignore_discard=True, ignore_expires=True)  # 保存cookie到cookie.txt中
        except TimeoutError as e:

            logging.error(e)
            raise Exception(e)

    def post_login_Adminweb(self, login_params,params):
        login_dic = {}
        try:
            headers = {
                'content-type': "application/x-www-form-urlencoded",
                'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
            }
            url = "http://bizcenter.sit.317hu.com/biz-center-web/bizcenter/loginReadRest/login"
            postdata = urllib.parse.urlencode(params).encode(encoding='UTF8')
            response = \
                requests.request("POST", url, headers=headers, data=postdata, verify=False)
            response.encoding = 'utf-8'
            response.raise_for_status()
            orginkey = 'success'
            if orginkey in response.text:
                login_response = json.loads(response.text)
                login_cookie = response.cookies
                login_dic.update({'roleIds': login_response['data']['roleIds']})
                login_dic.update({'userId': login_response['data']['userId']})
                login_dic.update({'cookie': login_cookie})
                logging.info('调用登录接口获取用户信息成功')
                return login_dic
        except TimeoutError as e:
            logging.error(e)
            raise Exception(e)

    def login_document(self, login_params, params):
        login_dic = {}
        cookie = "document_token=686010f06b8198a42639d0eca5cc3dfa;JSESSIONID=8CD34E68AC5BD528B2E37E0FFEA5771F"
        try:
            headers = {
                'content-type': "application/x-www-form-urlencoded",
                'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
                'Cookie' : "document_token=686010f06b8198a42639d0eca5cc3dfa;JSESSIONID=8CD34E68AC5BD528B2E37E0FFEA5771F"
            }
            url = self.hostsit_document + login_params['login_document']['url']
            postdata = utils.parse_urlparams(params)
            response = \
                requests.request("POST", url, headers=headers, data=postdata, verify=False)
            response.encoding = 'utf-8'
            response.raise_for_status()
            login_cookie = response.cookies
            login_dic.update({'cookie': cookie})
            logging.info('调用登录接口获取用户信息成功')
            return login_dic
        except TimeoutError as e:
            logging.error(e)
            raise Exception(e)
    #
    # def getGenernateKey(self, login_params):
    #     '''获取公钥密码'''
    #     publicKey = ""
    #     self.url = self.hostsit_document + login_params['generatePublicKey']['url']
    #     self.headers = {
    #         'Content-Type': "application/json",
    #         'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
    #     }
    #     response_passed = requests.request("POST", self.url, headers=self.headers)
    #     utils.checkRespMore(response_passed, self.url)
    #     if json.loads(response_passed.text)['data']:
    #         publicKey = json.loads(response_passed.text)['data']
    #     return publicKey

# if __name__ == "__main__":
#
#     m = Login()
#     m.post_login(login_info)


