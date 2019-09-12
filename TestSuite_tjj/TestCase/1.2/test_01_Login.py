#!C:\Program Files\Python36 python
# -*- coding: utf-8 -*-

'''
@author: yinzi
Project:登录界面
'''
import readConfig as readConfig
from Public.Utils import utils
import unittest
import sys
import requests

import datetime
case_path = sys.path[0]
localReadConfig = readConfig.ReadConfig()
class loginTjj(unittest.TestCase):
    '''登录界面'''
    @classmethod
    def setUpClass(cls):
        cls.UserAgent = localReadConfig.get_http("UserAgent")
        cls.userName = localReadConfig.get_http("userName")
        cls.password = localReadConfig.get_http("password")
        cls.nowtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        cls.Token = utils().getToken()

    @classmethod
    def tearDownClass(cls):
        print('test end')

    def test_01_tenantList(self):
        '''企业查询'''
        global tenantData# 所有企业信息
        url_part = "/admin/tenant/list"
        tenantData = utils().getRequest(url_part,Token=self.Token)

    def test_02_userInfo(self):
        '''获取权限信息'''
        global userData# 用户权限信息
        url_part = "/admin/user/info"
        userData = utils().getRequest(url_part,Token=self.Token)




if __name__ == "__main__":

    unittest.main()
    # 流程说明
    # 流程结束
