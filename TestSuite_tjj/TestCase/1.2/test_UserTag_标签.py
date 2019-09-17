#!C:\Program Files\Python36 python
# -*- coding: utf-8 -*-

'''
Created on 2019/8/5
@author: yinzi
Project:用户标签
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
class userTag(unittest.TestCase):
    '''用户标签'''
    @classmethod
    def setUpClass(cls):
        cls.UserAgent = localReadConfig.get_http("UserAgent")
        cls.dmp = localReadConfig.get_http("dmp")
        cls.projectId = 1
        cls.projectCode = "test_tjj"
        cls.userTagCode = "je"
        # cls.userTagName = "testTixianName3"
        cls.nowtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        cls.beforetime = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(days=30), '%Y-%m-%d %H:%M:%S')
        cls.Token = utils().getToken()

    @classmethod
    def tearDownClass(cls):
        print('test end')
    #
    # def test_01_usertagtype(self):
    #     '''创建标签分类'''
    #     global tagTypeName
    #     tagTypeName = "yinziTest"
    #     url_part = self.dmp + "/usertagtype"
    #     data = {
    #         "createTime": self.nowtime,
    #         "name": tagTypeName,
    #         "projectId": 1,
    #         "updateTime":""
    #     }
    #     utils().postRequest(url_part,Content_type="json",data=data, Token=self.Token)
    #
    # def test_0201_usertagtype(self):
    #     '''标签分类查询'''
    #     global usertagtype
    #     url_part = self.dmp + "/usertagtype/"+str(self.projectId)
    #     usertagtype = utils().getRequest(url_part,Token=self.Token)
    #
    # def test_0202_metaeventtype(self):
    #     '''元事件分类查询'''
    #     global eventtypes
    #     url_part = self.dmp + "/metaeventtype/byprojectid/"+str(self.projectId)
    #     eventtypes = utils().getRequest(url_part,Token=self.Token)
    #
    # def test_0203_metaeventtype(self):
    #     '''元事件分类编辑'''
    #     global eventtypes
    #     url_part = self.dmp + "/metaeventtype/byprojectid/"+str(self.projectId)
    #     eventtypes = utils().getRequest(url_part,Token=self.Token)
    #
    # def test_0201_metaeventtype(self):
    #     '''元事件查询'''
    #     global events
    #     for eventtype in eventtypes:
    #         if eventtype['name'] == "充值提现":
    #             url_part = self.dmp + "/metaevent/page?current=1&size=10&typeId="+str(eventtype['id'])
    #     events = utils().getRequest(url_part,Token=self.Token)
    #
    # def test_0202_metaeventtype(self):
    #     '''元事件详情'''
    #     global event
    #     for event in events:
    #         if event['code'] == 'tixian':
    #             url_part = self.dmp + "/metaevent/info/"+str(event['id'])
    #     event = utils().getRequest(url_part,Token=self.Token)
    #
    # def test_03_usertaglayer(self):
    #     '''新增用户标签'''
    #     url_part = self.dmp + "/usertag"
    #     userTagLayerRule = { "existed": 1,
    #                          "metaEventPropertyId": event['metaEventProperties'][0]['id'],
    #                          "metaEventId": event['metaEvent']['id'],
    #                          "operateDictId": event['metaEventKeywords'][0]['operateDictId'],
    #                          "propertyValue": "30",
    #                          "startTime": self.beforetime,
    #                          "endTime": self.nowtime,
    #                         }
    #     for tagtype in usertagtype:
    #         if tagtype["name"] == "yinziTest":
    #             data = {
    #                       "userTag": {
    #                           "projectId": str(self.projectId),
    #                           "code": self.userTagCode,
    #                           "name": self.userTagName,
    #                           "userTagTypeId": tagtype['id'],
    #                           "version": 1.0
    #                       },
    #                       "userTagLayerComplete": [
    #                         {
    #                           "userTagLayer": {
    #                             "name": "userTagLayer",
    #                             "relationDictId": 1
    #                           },
    #                           "userTagLayerRule": [userTagLayerRule]
    #                         }
    #                       ]
    #                     }
    #     utils().postRequest(url_part,Content_type="json",data=data, Token=self.Token)

    def test_04_usertag(self):
        '''标签查询'''
        global userTagForExcel#用于Excel导出的标签数据
        url_part = self.dmp + "/usertag/byprojectcode?projectCode="+self.projectCode
        tags = utils().getRequest(url_part, Token=self.Token)
        for tag in tags:
            if tag['code'] == self.userTagCode:
                userTagForExcel = tag
                break

    def test_05_usertagExcel(self):
        '''标签人群包导出'''
        url_part = self.dmp + "/usertag/excel?id="+str(userTagForExcel['id'])
        utils().getRequestForExport(url_part, Token=self.Token)
        print(1)


if __name__ == "__main__":

    unittest.main()
    # 流程说明
    # 流程结束
