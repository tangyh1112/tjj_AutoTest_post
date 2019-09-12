#!C:\Program Files\Python36 python
# -*- coding: utf-8 -*-

'''
@author: yinzi
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
class Project(unittest.TestCase):
    '''项目管理'''
    @classmethod
    def setUpClass(cls):
        cls.UserAgent = localReadConfig.get_http("UserAgent")
        cls.projectCode = localReadConfig.get_http("projectCode")
        cls.projectId = localReadConfig.get_http("projectId")
        cls.nowtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        cls.beforetime = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(days=30), '%Y-%m-%d %H:%M:%S')
        cls.Token = utils().getToken()

    @classmethod
    def tearDownClass(cls):
        print('test end')

    def test_02_modelPage(self):
        '''模型管理分页查询'''
        global CalModel
        url_part = "/dmp/projectmodel/page?projectId="+str(self.projectId)
        modelPageList = utils().getRequest(url_part, Token=self.Token)
        for model in modelPageList:
            if model['name'].find('testCAL') != -1:
                CalModel = model

if __name__ == "__main__":

    unittest.main()
    # 流程说明
    # 流程结束
