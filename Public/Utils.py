#!C:\Users\dell\AppData\Local\Programs\Python\Python35 python
# -*- coding: utf-8 -*-
'''
Project:工具类
'''
import json
import requests
import logging
import datetime, time
import os
import impala.dbapi as ipdb
import readConfig as readConfig
localReadConfig = readConfig.ReadConfig()

#工具类
class utils:

    def __init__(self):
        '''初始加载参数，全局调用'''
        global Token
        self.host = localReadConfig.get_http("host")
        self.UserAgent = localReadConfig.get_http("UserAgent")

    # 带？ dict 拼接url
    def parse_url(data={}):
        item = data.items()
        urls = "?"
        for i in item:
            (key, value) = i
            temp_str = key + "=" + str(value)
            urls = urls + temp_str + "&"
        urls = urls[:len(urls) - 1]
        return urls

    # 不带？ dict 拼接url
    def parse_urlparams(data={}):
        item = data.items()
        urls = ""
        for i in item:
            (key, value) = i
            temp_str = key + "=" + str(value)
            urls = urls + temp_str + "&"
        urls = urls[:len(urls) - 1]
        return urls

    # 确认返回结果的正确性,附带更多信息（补充url）
    def checkResp(response_passed, url):
        response_passed.encoding = 'utf-8'
        print(response_passed.text)
        response_passed.raise_for_status()
        result = json.loads(response_passed.text)
        if 'code' in result.keys():
            successOrFail = result['code']
            if str(successOrFail) == '0':
                logging.info(response_passed.text)
            else:
                raise response_passed.text

    def getRequest(self, url_part, params="", Token=""):
        '''GET请求+返回结果处理'''
        url = self.host + url_part
        requestData = ""
        self.headers = {'User-Agent': self.UserAgent,
                        'Authorization': Token['token_type'] + ' ' + Token['access_token']}
        if params == "":
            response_passed = requests.request("get", url, headers=self.headers)
        else:
            response_passed = requests.request("get", url, params=params, headers=self.headers)
        utils.checkResp(response_passed, url)
        data = json.loads(response_passed.text)['data']
        if data is not None:
            requestData = data
        return requestData

    def postRequest(self, url_part, Content_type="", data="", Token=""):
        '''POST请求+返回结果处理'''
        url = self.host + url_part
        requestData = ""
        self.headers = {'User-Agent': self.UserAgent,
                        'Authorization': Token['token_type'] + ' ' + Token['access_token']}
        Jsonheaders = {'User-Agent': self.UserAgent,
                       'Authorization': Token['token_type'] + ' ' + Token['access_token'],
                       'Content-type': "application/json;charset=UTF-8"}
        if data == "":
            if Content_type == "json":
                response_passed = requests.request("post", url, headers=Jsonheaders)
            else:
                response_passed = requests.request("post", url, headers=self.headers)
        else:
            if Content_type == "json":
                response_passed = requests.request("post", url, data=json.dumps(data), headers=Jsonheaders)
            else:
                response_passed = requests.request("post", url, data=data, headers=self.headers)
        utils.checkResp(response_passed, url)
        data = json.loads(response_passed.text)['data']
        if data is not None:
            requestData = data
        return requestData

    def putOrDelRequest(self, option="", url_part="", Content_type="", data="", Token=""):
        '''PUT/DELETE请求+返回结果处理'''
        url = self.host + url_part
        requestData = ""
        self.headers = {'User-Agent': self.UserAgent,
                        'Authorization': Token['token_type'] + ' ' + Token['access_token']}
        Jsonheaders = {'User-Agent': self.UserAgent,
                       'Authorization': Token['token_type'] + ' ' + Token['access_token'],
                       'Content-type': "application/json;charset=UTF-8"}
        if option:
            optionForRequest = option
        if data == "":
            if Content_type == "json":
                response_passed = requests.request(optionForRequest, url, headers=Jsonheaders)
            else:
                response_passed = requests.request(optionForRequest, url, headers=self.headers)
        else:
            if Content_type == "json":
                response_passed = requests.request(optionForRequest, url, data=json.dumps(data), headers=Jsonheaders)
            else:
                response_passed = requests.request(optionForRequest, url, data=data, headers=self.headers)
        utils.checkResp(response_passed, url)
        data = json.loads(response_passed.text)['data']
        if data is not None:
            requestData = data
        return requestData

    def postRequestForExport(self, url_part, Content_type="", data="", Token=""):
        '''导出的GET请求+返回结果处理'''
        url = self.host + url_part
        requestData = ""
        self.headers = {'User-Agent': self.UserAgent,
                        'Authorization': Token['token_type'] + ' ' + Token['access_token']}
        Jsonheaders = {'User-Agent': self.UserAgent,
                       'Authorization': Token['token_type'] + ' ' + Token['access_token'],
                       'Content-type': "application/json;charset=UTF-8"}
        if data == "":
            if Content_type == "json":
                response_passed = requests.request("post", url, headers=Jsonheaders)
            else:
                response_passed = requests.request("post", url, headers=self.headers)
        else:
            if Content_type == "json":
                response_passed = requests.request("post", url, data=json.dumps(data), headers=Jsonheaders)
            else:
                response_passed = requests.request("post", url, data=data, headers=self.headers)
        if response_passed.status_code == 500:
            print(response_passed.text)
        else:
            Excel = response_passed.headers.get('Content-Disposition')
            ExcelMessage = Excel.split("=")
            name = ExcelMessage[-1]
            with open(name, "wb") as code:
                code.write(response_passed.content)
                print("下载生成成功：文件名为"+name)
            # if os.path.exists("exportTrain_country.xls"):
            #     print("pass")
            #     print("下载成功")
            #     os.remove("exportTrain_country.xls")
        return requestData

    def getToken(self):
        '''获取Token'''
        params = {"grant_type":"password", "username":"admin", "password":"123456"}
        url = "http://pamir-gateway:9999/auth/oauth/token"
        self.headers = {
            'User-Agent' : self.UserAgent,
            'Content-Type' : 'application/x-www-form-urlencoded',
            'Authorization' : 'Basic dGVzdDp0ZXN0'
        }
        response_passed = requests.request("post", url, data=params, headers=self.headers)
        utils.checkResp(response_passed, url)
        Token = json.loads(response_passed.text)
        print(Token)
        return Token

    def getOtherToken(self, url):
        '''获取第三方Token'''
        self.headers = {
            'User-Agent' : self.UserAgent
        }
        response_passed = requests.request("post", url, headers=self.headers)
        utils.checkResp(response_passed, url)
        Token = json.loads(response_passed.text)
        print(Token)
        return Token

    def connHive(sql):
        '''Hive查询'''
        conn = ipdb.connect(host='192.168.10.111', port=10000, user='hdfs', auth_mechanism='PLAIN')
        # 使用cursor()方法获取操作游标
        cursor = conn.cursor()
        # 异常处理
        HiveRequest = ""
        try:
            cursor.execute('''select to_date(sms_time),count(*)  as a from yz.sms_record where sign_name='比心'  and sms_time>='2019-08-09' and sms_time<='2019-08-27' group by to_date(sms_time)''')
            HiveRequest = cursor.fetchall()
        except Exception as e:
            # hive不支持事务
            raise e
        finally:
            cursor.close()
            # 关闭数据库连接
            conn.close()
        return HiveRequest

#时间公用方法
    #等待时间计算
    def timing(self, waitTime):
        minute = datetime.datetime.now().strftime('%M')
        remainder = int(minute)%int(waitTime)
        if remainder == 0:
            time.sleep(waitTime*60)#等待五分钟
        elif 0 < remainder < waitTime:
            sleepTime = int(waitTime) - remainder
            time.sleep(sleepTime*60)

    def get_1st_of_last_month(self):
        """
        获取上个月第一天的日期，然后加21天就是22号的日期
        :return: 返回日期
        """
        today = datetime.datetime.today()
        year = today.year
        month = today.month
        if month == 1:
            month = 12
            year -= 1
        else:
            month -= 1
        res = datetime.datetime(year, month, 1) + datetime.timedelta(days=21)
        res = res.strftime("%Y%m%d")
        return res

    def get_1st_of_next_month(self):
        """
        获取下个月的22号的日期
        :return: 返回日期
        """
        today = datetime.datetime.today()
        year = today.year
        month = today.month
        if month == 12:
            month = 1
            year += 1
        else:
            month += 1
        res = datetime.datetime(year, month, 1) + datetime.timedelta(days=21)
        return res

    def getYesterday(self):
        """
        获取昨天
        """
        today=datetime.date.today()
        oneday=datetime.timedelta(days=1)
        yesterday=today-oneday
        yesterday = yesterday.strftime("%Y%m%d")
        return yesterday

    def getYesterday_ymd(self):
        """
        180303
        """
        today=datetime.date.today()
        oneday=datetime.timedelta(days=1)
        yesterday=today-oneday
        yesterday = yesterday.strftime("%y%m%d")
        return yesterday

    def getDict(self, type="", Token=""):
        '''获取项目字典项信息'''
        url = "http://pamir-gateway:9999/admin/dict/type/"+type
        self.headers = {
            'User-Agent' : self.UserAgent,
            'Authorization': Token['token_type'] + ' ' + Token['access_token']
        }
        response_passed = requests.request("get", url, headers=self.headers)
        utils.checkResp(response_passed, url)
        Dict = json.loads(response_passed.text)['data']
        return Dict


    def postRequestKK(self, url_part, Content_type="", data="", Token=""):
        '''POST请求+返回结果处理'''
        url = url_part
        requestData = ""
        self.headers = {'User-Agent': self.UserAgent,
                        'Authorization': 'Bearer' + ' ' + 'bc334f4b-ab44-401d-8efd-bb03f721135b'}#Token['access_token']
        Jsonheaders = {'User-Agent': self.UserAgent,
                       'Authorization': 'Bearer' + ' ' + 'bc334f4b-ab44-401d-8efd-bb03f721135b', 'Content-type': 'application/json;charset=UTF-8'}#Token['access_token']
        print(Token)
        if data == "":
            if Content_type == "json":
                response_passed = requests.request("post", url, headers=Jsonheaders)
            else:
                response_passed = requests.request("post", url, headers=self.headers)
        else:
            if Content_type == "json":
                response_passed = requests.request("post", url, data=json.dumps(data), headers=Jsonheaders)
            else:
                response_passed = requests.request("post", url, data=data, headers=self.headers)
        utils.checkResp(response_passed, url)
        data = json.loads(response_passed.text)['data']
        if data is not None:
            requestData = data
        return requestData