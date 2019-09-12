#!C:\Program Files\Python36 python
# -*- coding: utf-8 -*-

'''
@author: yinzi
Project:行业
'''
import readConfig as readConfig
from Public.Utils import utils
import unittest
import sys
from Public.configDB import MyDB
import datetime
case_path = sys.path[0]
localReadConfig = readConfig.ReadConfig()
class industry(unittest.TestCase):
    '''用户标签'''
    @classmethod
    def setUpClass(cls):
        cls.projectId = localReadConfig.get_http("projectId")
        cls.database = localReadConfig.get_db("database2")
        cls.nowtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        cls.beforetime = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(days=30), '%Y-%m-%d %H:%M:%S')
        cls.Token = utils().getToken()

    @classmethod
    def tearDownClass(cls):
        print('test end')

    def test_0101_industrySave(self):
        '''
        新增行业:不重复Code
        '''
        global usedData
        for i in range(1, 30):
            eventnum = industry().getSqlResult()# 查询行业信息
            url_part = "/admin/industrysign/industry/save"
            data = {
                      "code": "testIndustryCode" + str(int(eventnum)+1),
                      "name": "testIndustry" + str(int(eventnum)+1)
                    }
            usedData = data
            utils().postRequest(url_part, Content_type="json", data=data, Token=self.Token)
    #
    # def test_0102_industrySave(self):
    #     '''
    #     新增行业:已存在的重复Code 会提示存在重复Code
    #     '''
    #     url_part = "/admin/industrysign/industry/save"
    #     data = usedData
    #     utils().postRequest(url_part, Content_type="json", data=data, Token=self.Token)
    #
    # def test_02_industryPage(self):
    #     '''行业信息查询'''
    #     global needIndustry# 行业
    #     url_part = "/admin/industrysign/industry/page?current=1&size=10"
    #     industryList = utils().getRequest(url_part,Token=self.Token)
    #     for industry in industryList['records']:
    #         if industry['name'] == usedData['name']:
    #             needIndustry = industry
    #
    # def test_03_industryCodes(self):
    #     '''根据编号查询行业'''
    #     global industryPage# 项目列表信息
    #     url_part = "/admin/industrysign/industry/codes?codes=" + str(usedData['code'])
    #     industryPage = utils().getRequest(url_part,Token=self.Token)
    #
    # def test_04_industryCodes(self):
    #     '''查询所有行业'''
    #     url_part = "/admin/industrysign/industry/all"
    #     utils().getRequest(url_part,Token=self.Token)
    #
    # def test_0501_industryCodes(self):
    #     '''
    #     修改行业：修改今日创建的行业
    #     '''
    #     url_part = "/admin/industrysign/industry"
    #     data = {
    #               "code": needIndustry['code'],
    #               "id": needIndustry['id'],
    #               "name": needIndustry['name']+"modify"
    #             }
    #     utils().putOrDelRequest(option="put", url_part=url_part, Content_type="json", data=data, Token=self.Token)
    #
    # def test_0502_industryCodes(self):
    #     '''
    #     修改行业：修改非今日创建的行业
    #     '''
    #     url_part = "/admin/industrysign/industry"
    #     data = {
    #               "code": needIndustry['code'],
    #               "id": needIndustry['id'],
    #               "name": needIndustry['name']+"modify"
    #             }
    #     utils().putOrDelRequest(option="put", url_part=url_part, Content_type="json", data=data, Token=self.Token)

    def getSqlResult(self):
        '''获取最新事件信息和属性信息'''
        query_param = ['%%%s%%' % 'testIndustry']
        eventsql = "SELECT description FROM sys_dict where description like %s order by id asc;"
        eventResult = MyDB().executeSQL(eventsql, query_param, database=self.database)
        if eventResult:
            event = eventResult.split("testIndustry")
            if event[1] == "":
                eventnum = 0
            else:
                if event[1].find('modify') != -1:
                    num = event[1].split("modify")
                    eventnum = num[0]
                else:
                    eventnum = event[1]
        else:
            eventnum = 0
        return eventnum


if __name__ == "__main__":

    unittest.main()
    # 流程说明
    # 流程结束
