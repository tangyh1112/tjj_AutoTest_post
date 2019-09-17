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
        cls.nowtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        cls.beforetime = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(days=30), '%Y-%m-%d %H:%M:%S')
        cls.Token = utils().getToken()

    @classmethod
    def tearDownClass(cls):
        print('test end')

    def test_0101_exportExcel(self):
        '''
        人群包导出 签名+事件+口径
        '''
        statisticalCaliberList = ["total_amount","user_amount","average_amount"]
        part = self.dmp + "/metaevent/userBag"
        for statisticalCaliber in statisticalCaliberList:
            data = {"projectCode":"test_tjj","projectId":1,"signName":"YY语音","simpleAnalysis":"false",
                    "startTime":"2019-08-08 00:00:00","endTime":"2019-08-11 00:00:00",
                    "metaEventCode": "tixian2", "statisticalCaliber": statisticalCaliber}
            url_part = part + utils.parse_url(data)
            print("签名+事件+口径"+statisticalCaliber)
            utils().getRequestForExport(url_part, data=data, Token=self.Token)

    def test_0102_exportExcel(self):
        '''
        人群包导出 事件+口径
        '''
        statisticalCaliberList = ["total_amount","user_amount","average_amount"]
        part = self.dmp + "/metaevent/userBag"
        for statisticalCaliber in statisticalCaliberList:
            data = {"projectCode":"test_tjj","projectId":1,"signName":"","simpleAnalysis":"false",
                    "startTime":"2019-08-08 00:00:00","endTime":"2019-08-11 00:00:00",
                    "metaEventCode": "tixian2", "statisticalCaliber": statisticalCaliber}
            url_part = part + utils.parse_url(data)
            print("事件+口径"+statisticalCaliber)
            utils().getRequestForExport(url_part, data=data, Token=self.Token)

    def test_0103_exportExcel(self):
        '''
        人群包导出 签名+简单分析
        '''
        part = self.dmp + "/metaevent/userBag"
        data = {"projectCode":"test_tjj","projectId":1,"signName":"YY语音","simpleAnalysis":"true",
                "startTime":"2019-08-08 00:00:00","endTime":"2019-08-11 00:00:00",
                "metaEventCode": "", "statisticalCaliber": ""}
        url_part = part + utils.parse_url(data)
        print("签名+简单分析")
        utils().getRequestForExport(url_part, data=data, Token=self.Token)


if __name__ == "__main__":

    unittest.main()
    # 流程说明
    # 流程结束
