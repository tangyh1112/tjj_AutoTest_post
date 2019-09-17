#!C:\Program Files\Python36 python
# -*- coding: utf-8 -*-

'''
@author: yinzi
'''
import readConfig as readConfig
from Public.Utils import utils
import unittest
import sys
from Public.configDB import MyDB
import datetime
case_path = sys.path[0]
localReadConfig = readConfig.ReadConfig()
class tableSearch(unittest.TestCase):
    '''库管理'''
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

    def test_01_table(self):
        '''
        表查询
        '''
        url_part = self.dmp + "/warehouse/tables?projectId={}".format(self.projectId, "event_record")
        utils().getRequest(url_part, Token=self.Token)

    def test_02_tablerecord(self):
        '''
        表字段查询
        '''
        url_part = self.dmp + "/warehouse/tablerecord?projectId={}&tableName={}".format(self.projectId, "key_words")
        utils().getRequest(url_part, Token=self.Token)

if __name__ == "__main__":

    unittest.main()
    # 流程说明
    # 流程结束
