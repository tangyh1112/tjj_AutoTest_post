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
        cls.nowtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        cls.beforetime = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(days=30), '%Y-%m-%d %H:%M:%S')
        url="http://pamir-gateway:9999/dmp/auth/token?app_id=admin&app_secret=123456"
        cls.Token = utils().getOtherToken(url=url)

        # cls.Token = utils().getToken()

    @classmethod
    def tearDownClass(cls):
        print('test end')

    def test_01_smschannel(self):
        '''短信通道分页查询'''
        global reportsourceList
        url_part = "http://pamir-gateway:9999/dmp/1/audience/sports/update/"
        data = {
                    "audience_list": [{
                            "gid": "103",
                            "mobile": "13758471471",
                            "audience_id": 1,
                            "is_import": "true",
                            "fail_reason": "",
                            "biz": [{
                                    "biz_type": 5,
                                    "biz_time": "2019-08-19 14:12:12"
                                },
                                {
                                    "biz_type": 5,
                                    "biz_time": "2019-08-21 14:12:12"
                                }
                            ]
                        },
                        {
                            "gid": "104",
                            "mobile": "18989848397",
                            "audience_id": 2,
                            "is_import": "true",
                            "fail_reason": "",
                            "biz": [{
                                    "biz_type": 1,
                                    "biz_time": "2019-08-11 08:30:10"
                                }, {
                                    "biz_type": 2,
                                    "biz_time": "2019-08-15 21:40:20"
                                },
                                {
                                    "biz_type": 3,
                                    "biz_time": "2019-08-16 16:34:28"
                                }
                            ]
                        }
                    ]
                }

        reportsourceList = utils().postRequestKK(url_part, Content_type="json", data=data, Token=self.Token)

    def test_02_smschannel(self):
        '''短信通道分页查询'''
        global reportsourceList
        url_part = "http://pamir-gateway:9999/dmp/1/audience/sports/update_consume/"
        data = {
                    "audience_list": [{
                            "gid": "101",
                            "mobile": "13758471471",
                            "audience_id": 1,
                            "year": 2019,
                            "month": 9,
                            "total_money": 35475.25,
                            "total_consume": 5,
                            "biggest_consume": 1540.00,
                            "user_status": 4
                        }
                    ]
                }
        reportsourceList = utils().postRequestKK(url_part, Content_type="json", data=data, Token=self.Token)

if __name__ == "__main__":

    unittest.main()
    # 流程说明
    # 流程结束
