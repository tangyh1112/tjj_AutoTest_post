#!C:\Program Files\Python36 python
# -*- coding: utf-8 -*-

'''
@author: yinzi
Project:用户分群
'''
import readConfig as readConfig
from Public.Utils import utils
import unittest
import sys
from Public.configDB import MyDB
import datetime
case_path = sys.path[0]
localReadConfig = readConfig.ReadConfig()
class userBag(unittest.TestCase):
    '''用户标签'''
    @classmethod
    def setUpClass(cls):
        cls.projectId = localReadConfig.get_http("projectId")
        cls.projectId = localReadConfig.get_http("dmp")
        cls.projectCode = localReadConfig.get_http("projectCode")
        cls.database = localReadConfig.get_db("database1")
        cls.userTagCodes = [] #待选择的标签，如果不填，则默认选择20个code
        cls.nowtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        cls.Token = utils().getToken()

    @classmethod
    def tearDownClass(cls):
        print('test end')
    @unittest.skip("暂时跳过")
    def test_01_usertag(self):
        '''标签查询'''
        global userTagCodeList
        userTagCodeList = []
        url_part = "/dmp/usertag/byprojectcode?projectCode="+self.projectCode
        tags = utils().getRequest(url_part, Token=self.Token)
        for tag in tags:
            if self.userTagCodes == '':
                for userTagCode in self.userTagCodes:
                    if tag['code'] == userTagCode:
                        userTagCodeList.append(tag)
            else:
                count = 0
                if count < 20:
                    userTagCodeList.append(tag)
                    count += 1
                else:
                    break
    @unittest.skip("暂时跳过")
    def test_02_userBag(self):
        '''创建分群'''
        tagLayerId = []
        url_part = "/dmp/personprofile"
        sqlResult = userBag().getSqlResult()
        for userTagCode in userTagCodeList:
            tagLayerId.append(userTagCode['userTagLayerCompleteDTO'][0]['id'])
        tagLayerIds = ','.join('%s' % str(id) for id in tagLayerId)
        data = {
                  "code": sqlResult[0],
                  "name": sqlResult[1],
                  "projectId": self.projectId,
                  "tagLayerId": tagLayerIds
                }
        utils().postRequest(url_part,Content_type="json",data=data,Token=self.Token)
    @unittest.skip("暂时跳过")
    def test_03_personprofilePage(self, nameUsed=""):
        '''分页查询'''
        global personprofile
        nameList = ["","test"]
        if nameUsed == "":
            for name in nameList:
                url_part = "/dmp/personprofile/page?current=1&size=20&name={}&projectId={}".format(name, self.projectId)
        else:
            url_part = "/dmp/personprofile/page?current=1&size=20&name={}&projectId={}".format(nameUsed, self.projectId)
        personprofile = utils().getRequest(url_part, Token=self.Token)

    @unittest.skip("暂时跳过")
    def test_04_userBag(self):
        '''
        修改分群
        修改内容：1.code；2.name,3.标签分层
        '''
        url_part = "/dmp/personprofile"
        modifyCotentList = ['name', 'tagLayerId']#, 'code'
        modifyId = personprofile[0]['id']
        data = {
                  "code": personprofile[0]['code'],
                  "createTime": personprofile[0]['createTime'],
                  "deleteFlag": personprofile[0]['deleteFlag'],
                  "id": personprofile[0]['id'],
                  "name": personprofile[0]['name'],
                  "projectId": personprofile[0]['projectId'],
                  "tagLayerId": personprofile[0]['tagLayerId'],
                  "updateTime": self.nowtime,
                  "version": personprofile[0]['version']
                }

        for modifyCotent in modifyCotentList:
            if modifyCotent == 'code':
                data['code'] = data['code'] + "modify"
            if modifyCotent == 'name':
                data['name'] = data['name'] + "modify"
            if modifyCotent == 'tagLayerId':
                tagLayerIdList = data['tagLayerId'].split(",")
                tagLayerIdList.remove(tagLayerIdList[0])
                tagLayerId = ','.join('%s' % str(id) for id in tagLayerIdList)
                data['tagLayerId'] = tagLayerId # 暂时不修改
            utils().putOrDelRequest(option="put", url_part=url_part, Content_type="json", data=data, Token=self.Token)
            userBag().test_03_personprofilePage(data['name']) # 查询修改情况，做版本判断
            for page in personprofile:
                if page['id'] == modifyId:
                    print("version="+str(page['version']))

    def test_05_exportPerson(self):
        '''导出人群包'''
        # for i in range(1, 30):
        url_part = "/dmp/personprofile/userBag"
        data = {"code":'jeFQ', "projectCode":self.projectCode,"projectId":self.projectId}
        # data = {"code":personprofile[0]['code'], "projectCode":self.projectCode,"projectId":self.projectId}
        url_part = url_part + utils.parse_url(data)
        utils().getRequestForExport(url_part, Token=self.Token)
            # print(i)

    def getSqlResult(self):
        '''获取最新事件信息和属性信息'''
        query_param = ['%%%s%%' % 'testFQ']
        eventsql = "SELECT name FROM dmp_person_profile where name like %s order by id asc;"
        eventResult = MyDB().executeSQL(eventsql, query_param, database=self.database)
        if eventResult:
            event = eventResult.split("testFQName")
            if event[1] == "":
                eventnum = 0
            else:
                if event[1].find('modify'):
                    num = event[1].split("modify")
                    eventnum = num[0]
                else:
                    eventnum = event[1]

        else:
            eventnum = 0
        testFQCode = "testFQCode" + str(int(eventnum) + 1)
        testFQName = "testFQName" + str(int(eventnum) + 1)
        sqlResult = [testFQCode, testFQName]
        return sqlResult

if __name__ == "__main__":

    unittest.main()
    # 流程说明
    # 流程结束
