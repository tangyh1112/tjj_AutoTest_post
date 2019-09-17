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
        cls.userId = localReadConfig.get_http("userId")
        cls.nowtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        cls.beforetime = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(days=30), '%Y-%m-%d %H:%M:%S')
        cls.partitionDay = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(days=22), '%Y-%m-%d 00:00:00')
        cls.signName = ""#比心
        cls.sampleTypeList = [1,2,3]#1:特征随机，2：按时间最晚，3：按时间最早
        cls.Token = utils().getToken()

    @classmethod
    def tearDownClass(cls):
        print('test end')

    def test_01_reportsource(self):
        '''源数据统计结果'''
        global reportsourceList
        data = {"endTime":self.beforetime,"projectId":self.projectId,"signName":self.signName,"startTime":self.nowtime}
        url_part = self.dmp + "/reportsource" + utils.parse_url(data)
        reportsourceList = utils().getRequest(url_part,Token=self.Token)

    def test_02_Hivereport(self):
        '''hive查询结果'''
        global hiveList# 项目列表信息
        sql = "select to_date(sms_time),count(*)  as a from sms_record where sign_name='比心' and sms_time>='2019-08-09' and sms_time<='2019-08-27' group by to_date(sms_time)"
        hiveList = utils.connHive(sql)

    def test_03_compare(self):
        '''查询结果比对'''
        for reportsource in reportsourceList:
            for hive in hiveList:
                if reportsource['date'] == list(hive)[0]:
                    if reportsource['value'] == list(hive)[1]:
                        print("pass")
                    else:
                        print("fail:"+str(reportsource['date'])+"value="+str(reportsource['value'])+"，实际为："+str(list(hive)[1]))

    def test_04_sample(self):
        '''取样'''
        global reportsourceList
        sampleCountList = ["","1","2000","5000","5001"]
        for sampleType in self.sampleTypeList:
            for sampleCount in sampleCountList:
                data = {
                          "operateId": self.userId,
                          "partitionDay": self.partitionDay,
                          "projectId": self.projectId,
                          "sampleCount": sampleCount,
                          "sampleType": sampleType,
                          "signName": self.signName
                        }
                url_part = self.dmp + "-aly/sample"
                utils().getRequestForExport(url_part, data=data, Token=self.Token)

if __name__ == "__main__":

    unittest.main()
    # 流程说明
    # 流程结束
