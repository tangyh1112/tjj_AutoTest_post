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
        eventnum = industry().getSqlResult()# 查询行业信息
        url_part = "/admin/industrysign/industry/save"
        # data = {
        #           "code": "testSignCode" + str(int(eventnum)+1),
        #           "name": "testSign" + str(int(eventnum)+1)
        #         }
        data = {
            "code": "testSignCode" + str(int(eventnum) + 1),
            "name": "testSign" + str(int(eventnum)+1)
        }
        usedData = data
        utils().postRequest(url_part, Content_type="json", data=data, Token=self.Token)

    def getSqlResult(self):
        '''获取最新事件信息和属性信息'''
        query_param = ['%%%s%%' % 'testSign']
        eventsql = "SELECT description FROM sys_dict_item where description like %s order by id asc;"
        eventResult = MyDB().executeSQL(eventsql, query_param, database=self.database)
        if eventResult:
            event = eventResult.split("testSign")
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
