#!C:\Program Files\Python36 python
# -*- coding: utf-8 -*-

'''
@author: yinzi
Project:模型管理-计算
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
        cls.dmp = localReadConfig.get_http("dmp")
        cls.projectId = localReadConfig.get_http("projectId")
        cls.nowtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        cls.beforetime = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(days=30), '%Y-%m-%d %H:%M:%S')
        cls.tableName = "sms_split"
        cls.Token = utils().getToken()

    @classmethod
    def tearDownClass(cls):
        print('test end')

    # @unittest.skip("创建已完成，暂不创建")
    # def test_01_projectmodel(self):
    #     '''创建模型'''
    #     url_part = self.dmp + "/projectmodel"
    #     modelDictIds = utils().getDict(type="model_type", Token=self.Token)
    #     modelDictIds.pop()
    #     for modelDictId in modelDictIds:
    #         if modelDictId['label'] == '计算模型':
    #             data = {
    #                       "code": "test"+modelDictId['value']+"Code",
    #                       "modelDictId": modelDictId['id'],
    #                       "name": "test"+modelDictId['value']+"Name",
    #                       "projectId": self.projectId
    #                     }
    #             utils().postRequest(url_part,Content_type="json",data=data, Token=self.Token)

    def test_02_modelPage(self):
        '''模型管理分页查询'''
        global CalModel
        url_part = self.dmp + "/projectmodel/page?projectId="+str(self.projectId)
        modelPageList = utils().getRequest(url_part, Token=self.Token)
        for model in modelPageList:
            if model['name'].find('testCAL') != -1:
                CalModel = model

    def test_03_projectmodelcal(self):
        '''计算模型设置'''
        url_part = self.dmp + "/projectmodelcal"
        data = {
                  "modelId": CalModel['id'],
                  "projectId": self.projectId
                }
        utils().putOrDelRequest(option="put", url_part=url_part, Content_type="json", data=data, Token=self.Token)

if __name__ == "__main__":

    unittest.main()
    # 流程说明
    # 流程结束
