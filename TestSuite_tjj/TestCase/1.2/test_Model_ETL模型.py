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
    def test_01_projectmodel(self):
        '''创建模型'''
        url_part = self.dmp + "/projectmodel"
        modelDictIds = utils().getDict(type="model_type", Token=self.Token)
        modelDictIds.pop()
        # for modelDictId in modelDictIds:
        data = {
                  "code": "testETLCode24",
                  "modelDictId": modelDictIds[0]['id'],
                  "name": "testETLName24",
                  "projectId": self.projectId
                }
        utils().postRequest(url_part,Content_type="json",data=data, Token=self.Token)

    def test_02_modelPage(self):
        '''模型管理分页查询'''
        global modelPageList
        url_part = self.dmp + "/projectmodel/page?projectId="+str(self.projectId)
        modelPageList = utils().getRequest(url_part, Token=self.Token)

    @unittest.skip("创建已完成，暂不创建")
    def test_03_modelPage(self):
        '''修改模型'''
        url_part = self.dmp + "/projectmodel"
        data = {
                  "code": "testETLCode",
                  "createTime": modelPageList[0]['createTime'],
                  "deleteFlag": modelPageList[0]['deleteFlag'],
                  "id": modelPageList[0]['id'],
                  "modelDictId": modelPageList[0]['modelDictId'],
                  "name": "testETLName",#modelPageList[0]['name'],
                  "projectId": self.projectId
                }
        utils().putOrDelRequest(option="put", url_part=url_part, Content_type="json", data=data, Token=self.Token)

    def test_04_modelPage(self):
        '''编辑查询单模型'''
        global modelTable #待处理的表模型
        url_part = self.dmp + "/projectmodel/"+str(modelPageList[0]['id'])
        projectModelInstenceList = utils().getRequest(url_part, Token=self.Token)
        for table in projectModelInstenceList['projectModelInstence']['tables']:
            if table['tableName'] == self.tableName:
                modelTable = table
                break

    @unittest.skip("暂不删除")
    def test_05_modelPage(self):
        '''删除模型'''
        url_part = self.dmp + "/projectmodel/"+str(modelPageList[0]['id'])
        utils().putOrDelRequest(option="delete", url_part=url_part, Token=self.Token)

    def test_06_modelPage(self):
        '''查询表字段信息'''
        url_part = self.dmp + "/projectmodeletl/hive/"+self.tableName
        utils().getRequest(url_part, Token=self.Token)

    def test_07_modelPage(self):
        '''设置ETL'''
        url_part = self.dmp + "/projectmodeletl"
        data = {
                  "modelId": modelPageList[0]['id'],
                  "projectId": self.projectId,
                  "tables": [
                    {
                      "rules": [{
                                  "field": "sign_name",
                                  "operator": "equal",
                                  "value": "交易猫1"
                                }],
                      "setUp": "true",
                      "tableName": self.tableName,#"sms_record"
                      "targetTableName": "string"
                    }
                  ]
                }
        utils().putOrDelRequest(option="put", url_part=url_part, Content_type="json", data=data, Token=self.Token)
        Model().test_02_modelPage()
        version = modelPageList[0]['projectModelInstence']['version']
        print(version)

    def test_08_projectmodeletl(self):
        '''任务调用，并生成脚本'''
        url_part = self.dmp + "/projectmodel/model/" + str(modelPageList[0]['id'])
        utils().getRequest(url_part, Token=self.Token)

if __name__ == "__main__":

    unittest.main()
    # 流程说明
    # 流程结束
