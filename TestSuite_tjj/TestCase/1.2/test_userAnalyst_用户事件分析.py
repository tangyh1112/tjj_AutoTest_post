#!C:\Program Files\Python36 python
# -*- coding: utf-8 -*-

'''
@author: yinzi
Project:用户事件分析
'''
import readConfig as readConfig
from Public.Utils import utils
import unittest
import sys
from Public.configDB import MyDB
import datetime
case_path = sys.path[0]
localReadConfig = readConfig.ReadConfig()
class userAnalyst(unittest.TestCase):
    '''用户事件分析'''
    @classmethod
    def setUpClass(cls):
        cls.projectId = localReadConfig.get_http("projectId")
        cls.dmp = localReadConfig.get_http("dmp")
        cls.signNameForSearch = "雷" #签名模糊查询的参数
        cls.signName = "比心" #签名模糊查询的参数
        cls.eventtypeName = "测试带属性的元事件" #hive中存在数据的元事件分类名称--用于查询
        cls.eventName = "带提的" #hive中存在数据的元事件名称--用于查询
        cls.nowtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        cls.beforetime = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(days=20), '%Y-%m-%d %H:%M:%S')
        cls.Token = utils().getToken()

    @classmethod
    def tearDownClass(cls):
        print('test end')


    def test_01_projectinfoPage(self):
        '''项目列表信息'''
        global project# 项目信息
        project = ""
        url_part = self.dmp + "/projectinfo/page?current=1&size=20"
        projectinfoPageList = utils().getRequest(url_part,Token=self.Token)
        for projectinfo in projectinfoPageList['projectInfoPage']['records']:
            if str(projectinfo['id']) == self.projectId:
                project = projectinfo

    # def test_02_signPage(self):
    #     '''分页查询签名'''
    #     global sign# 项目列表信息
    #     url_part = "/admin/industrysign/sign/page"
    #     data = {
    #               "current":1,
    #               "industryCodes": [
    #                 project['industryGroup']
    #               ],
    #               "signName": self.signNameForSearch,
    #               "size": 1000
    #             }
    #     signPageList = utils().postRequest(url_part,Content_type="json",data=data, Token=self.Token)
    #     for signPage in signPageList['records']:
    #         if signPage['signName'] == self.signName:
    #             sign = signPage
    #
    # def test_03_eventtype(self):
    #     '''元事件分类查询'''
    #     global eventtype# 元事件分类
    #     eventtype = ""
    #     url_part = self.dmp + "/metaeventtype/byprojectid/" + str(self.projectId)
    #     eventtypeList = utils().getRequest(url_part, Token=self.Token)
    #     if eventtypeList:
    #         for type in eventtypeList:
    #             if type['name'] == self.eventtypeName:
    #                 eventtype = type
    #
    # def test_04_eventtype(self):
    #     '''元事件查询'''
    #     global event# 元事件
    #     url_part = self.dmp + "/metaevent/bytypeid/" + str(eventtype['id'])
    #     eventList = utils().getRequest(url_part, Token=self.Token)
    #     if eventList:
    #         for ev in eventList:
    #             if ev['name'] == self.eventName:
    #                 event = ev
    #
    def test_0501_analysis(self):
        '''
        用户事件分析查询
        1.简单分析：签名+日期'''
        global simpleanalysisdata
        url_part = self.dmp + "/metaevent/analysis"#sign['signName']
        simpleanalysisdata = {"projectCode":project['code'],"projectId":project['id'],"signName": self.signName, "simpleAnalysis":True, "startTime":str(self.beforetime),"endTime":str(self.nowtime)}
        print(simpleanalysisdata)
        # utils().postRequest(url_part, Content_type="json", data=simpleanalysisdata, Token=self.Token)
    #
    # def test_0502_analysis(self):
    #     '''
    #     用户事件分析查询
    #     1.用户事件分析：签名(可有可无)+日期+事件+口径'''
    #     global analysisdata
    #     url_part = self.dmp + "/metaevent/analysis"
    #     statisticalCaliberList = ["total_amount","user_amount","average_amount"] # 总次数/用户数/人均次数
    #     signNameList = ["",self.signName] # 未选择签名/选择了某个签名（但不是简单分析） sign['signName']
    #     for statisticalCaliber in statisticalCaliberList:
    #         for signName in signNameList:
    #             data = {"projectCode":project['code'],"projectId":project['id'],"signName":self.signName,"simpleAnalysis":"false",
    #                     "current":1,"startTime":self.beforetime,"endTime":self.nowtime, "metaEventName": event['name'],
    #                     "metaEventCode": event['code'], "statisticalCaliber": statisticalCaliber}
    #             print("signName="+signName+",statisticalCaliber="+statisticalCaliber)
    #             analysisdata = data
    #             utils().postRequest(url_part, Content_type="json", data=data, Token=self.Token)

    # def test_0601_exportExcel(self):
    #     '''
    #     人群包导出
    #     1.未查询，提示：用户画像未生成
    #     '''
    #     url_part = self.dmp + "/metaevent/userBag"
    #     data = {"projectCode":project['code'],"projectId":project['id'],"signName":"盛趣游戏","simpleAnalysis":"false",
    #             "startTime":"2019-05-18 00:00:00","endTime":"2019-05-20 00:00:00",
    #             "metaEventCode": "tixian2", "statisticalCaliber": "total_amount"}
    #     print("除时间判断外，无任何条件，查询提示：用户画像记录未生成!")
    #     utils().getRequestForExport(url_part, data=data, Token=self.Token)
    #
    def test_0602_exportExcel(self):
        '''
        人群包导出
        2.简单分析导出
        '''
        url_part = self.dmp + "/metaevent/userBag"
        data = simpleanalysisdata
        print(data)
        print("简单分析")
        utils().postRequestForExport(url_part, Content_type="json",data=data, Token=self.Token)


if __name__ == "__main__":

    unittest.main()
    # 流程说明
    # 流程结束
