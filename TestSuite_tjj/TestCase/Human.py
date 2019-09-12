#!C:\Program Files\Python36 python
# -*- coding: utf-8 -*-

'''
@author: yinzi
Project:模型管理
'''
import readConfig as readConfig
from Public.Utils import utils
import unittest
import sys
import json
import requests
import datetime
case_path = sys.path[0]
localReadConfig = readConfig.ReadConfig()
class Model(unittest.TestCase):
    '''模型管理'''
    @classmethod
    def setUpClass(cls):
        cls.UserAgent = localReadConfig.get_http("UserAgent")
        cls.projectCode = localReadConfig.get_http("projectCode")
        cls.projectId = localReadConfig.get_http("projectId")
        cls.nowtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        cls.beforetime = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(days=30), '%Y-%m-%d %H:%M:%S')
        cls.tableName = "sms_split"
        cls.Token = utils().getToken()

    @classmethod
    def tearDownClass(cls):
        print('test end')

    def test_01_projectmodel(self):
        '''/audiencepackage/userid 查询人群包的userId'''
        url_part = "/dmp/audiencepackage/userid"
        modelDictIds = utils().getDict(type="packageType", Token=self.Token)
        data1 = {
                  "current": 0,
                  "eventId": 0,
                  "numberLimit": 0,
                  "packageType": modelDictIds[0],
                  "partitionDayList": [
                    {
                      "operator": "string",
                      "value": "string"
                    }
                  ],
                  "projectId": 0,
                  "signName": "string",
                  "size": 0
                }
        data = {
                  "packageType": modelDictIds[0],
                  "partitionDayList": [
                    {
                      "operator": "string",
                      "value": "string"
                    }
                  ],
                  "projectId": 0,
                  "signName": "string",
                }
        utils().postRequest(url_part,Content_type="json",data=data, Token=self.Token)

    def test_08_projectmodeletl(self):
        '''任务调用，并生成脚本'''
        url_part = "/dmp/projectmodel/model/" + str(modelPageList[0]['id'])
        utils().getRequest(url_part, Token=self.Token)

if __name__ == "__main__":

    unittest.main()
    # 流程说明
    # 流程结束
