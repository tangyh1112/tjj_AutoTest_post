#!C:\Program Files\Python36 python
# -*- coding: utf-8 -*-

'''
Created on 2019/8/5
@author: yinzi
Project:元事件及关键词
'''
import readConfig as readConfig
from Public.Utils import utils
import unittest
import sys
import impala.dbapi as ipdb
import datetime
case_path = sys.path[0]
localReadConfig = readConfig.ReadConfig()
class eventRecord(unittest.TestCase):
    '''用户标签'''
    @classmethod
    def setUpClass(cls):
        cls.projectId = localReadConfig.get_http("projectId")
        cls.dmp = localReadConfig.get_http("dmp")
        cls.nowtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        cls.beforetime = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(days=30), '%Y-%m-%d %H:%M:%S')
        cls.Token = utils().getToken()

    @classmethod
    def tearDownClass(cls):
        print('test end')

    # def test_01_smschannel(self):
    #     '''添加短信通道'''
    #     for i in range(1, 30):
    #         data = {"isDefault":0,"isDisable":0,"name":"测试分页","code":"测试分页","surplusNumber":1000,"maxEachtimeNumber":1}
    #         url_part = self.dmp + "/smschannel"
    #         reportsourceList = utils().postRequest(url_part,Content_type="json",data=data,Token=self.Token)

    def test_02_smschannel(self):
        '''短信通道分页查询'''
        global reportsourceList
        url_part = self.dmp + "/smschannel/page?current=1&size=100"
        reportsourceList = utils().getRequest(url_part, Token=self.Token)

    def test_03_smschannel(self):
        '''添加短信通道'''
        global reportsourceList
        for reportsource in reportsourceList['records']:
            if reportsource['name'] == "测试分页":
                url_part = self.dmp + "/smschannel/"+str(reportsource['id'])
                reportsourceList = utils().putOrDelRequest(option="DELETE",url_part=url_part, Content_type="json",Token=self.Token)

if __name__ == "__main__":

    unittest.main()
    # 流程说明
    # 流程结束
