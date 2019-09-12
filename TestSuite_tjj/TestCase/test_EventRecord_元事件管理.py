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
from Public.configDB import MyDB
import datetime
case_path = sys.path[0]
localReadConfig = readConfig.ReadConfig()
class eventRecord(unittest.TestCase):
    '''用户标签'''
    @classmethod
    def setUpClass(cls):
        cls.projectId = localReadConfig.get_http("projectId")
        cls.database = localReadConfig.get_db("database1")
        cls.eventtypeName = "测试b"#"测试带属性的元事件"#元事件分类名称，如果这边写明了，则不再创建
        cls.eventName = ""#元事件名称，如果这边写明了，则不再创建
        cls.usedTypeId = ""#18 # 已经在hive中跑过的元事件分类ID
        cls.usedEventId = ""#55 # 已经在hive中跑过的元事件ID
        cls.propertyTypeDict = {"T":1,"N":2,"B":3,"D":4}
        cls.nowtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        cls.beforetime = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(days=30), '%Y-%m-%d %H:%M:%S')
        cls.Token = utils().getToken()

    @classmethod
    def tearDownClass(cls):
        print('test end')


    def test_01_projectinfoPage(self):
        '''项目列表信息'''
        global projectinfoPageList# 项目列表信息
        url_part = "/dmp-lt/projectinfo/page?current=1&size=20"
        projectinfoPageList = utils().getRequest(url_part,Token=self.Token)

    def test_02_metaeventtype(self):
        '''创建元事件分类'''
        global eventtypeName#元事件分类名称
        eventtypeName = self.eventtypeName
        if eventtypeName == "":#如果元事件分类名称没有，则新增
            eventtypeName = "测试"
            url_part = "/dmp-lt/metaeventtype"
            query_param = ['%%%s%%' % '测试']
            self.sql = "SELECT name FROM dmp_meta_event_type where name like %s order by id asc;"
            sqlResult = MyDB().executeSQL(self.sql, query_param, database=self.database)
            if sqlResult:
                Name = sqlResult.split("测试")
                if Name[1] == "":
                    num = "a"
                else:
                    num = "b"
            else:
                num = "c"
            eventtypeName = eventtypeName+num
            data = {
                "createTime": self.nowtime,
                "name": eventtypeName,
                "projectId": self.projectId
            }
            print(data)
            utils().postRequest(url_part, Content_type="json", data=data,Token=self.Token)

    def test_03_metaeventtype(self):
        '''查询元事件分类'''
        global eventType, allEventType#元事件分类名称
        url_part = "/dmp-lt/metaeventtype/byprojectid/" + str(self.projectId)
        requestData = utils().getRequest(url_part,Token=self.Token)
        if requestData:
            allEventType = requestData
            for data in requestData:
                if data['name'] == eventtypeName:
                    eventType = data
                    break

    def test_04_metaevent(self):
        '''创建元事件'''
        global sqlResult, metaEventData
        url_part = "/dmp-lt/metaevent"
        # for i in range(1, 30):
        sqlResult = eventRecord().getSqlResult()
        metaEventProperties = []
        keyList = list(self.propertyTypeDict.keys())
        valueList = list(self.propertyTypeDict.values())
        if self.eventName == "":
            for key in keyList:
                index = keyList.index(key)
                num = str(valueList[index])
                next = "a"
                Properties = {
                              "code": key+"test"+ next,
                              "name": key+"test"+ next,
                              "propertyType": str(num),
                              "sortNumber": str(num)
                            }
                metaEventProperties.append(Properties)
            data = {
                      "metaEvent": {
                        "code": sqlResult[0],
                        "description": "description",
                        "keywordRelation": "or",
                        "name": sqlResult[1],
                        "projectId": self.projectId,
                        "typeId": eventType['id'],
                        "version": 1.0
                      },
                      "metaEventKeywords": [
                        {
                          "operateDictId": 0,
                          "wordGroup": "短信,验证码"
                        },
                        {
                          "operateDictId": 0,
                          "wordGroup": "操作,有效"
                        }
                      ],
                      "metaEventProperties": metaEventProperties
                    }
            metaEventData = data
            print(metaEventData)
            utils().postRequest(url_part, Content_type="json", data=data, Token=self.Token)

    def test_05_metaevent(self):
        '''
        查询元事件
        1.根据分类ID查询元事件
        2.根据元事件ID查询元事件详细信息'''
        global event, eventContent#元事件
        url_part = "/dmp-lt/metaevent/page?current=1&size=10&typeId=" + str(eventType['id'])
        requestData = utils().getRequest(url_part, Token=self.Token)
        if requestData:
            for data in requestData['records']:
                if data['name'] == sqlResult[1]:
                    event = data
                    break

        url_part = "/dmp-lt/metaevent/info/" + str(event['id'])
        requestData = utils().getRequest(url_part, Token=self.Token)
        if requestData:
            eventContent = requestData

    def test_0601_metaevent(self):
        '''
        编辑元事件
        1.修改元事件基本信息（元事件名称、元事件显示名、元事件分类ID、描述），版本号不变
        '''
        global waitModifyEventData#修改过的元事件模板
        url_part = "/dmp-lt/metaevent"
        ModifyEventDataList = []
        waitModifyList = ["code", "name", "typeId", "description"]
        for waitModify in waitModifyList:
            if waitModify == "code":
                waitModifyEventData = eventRecord().makeupEventData()
                waitModifyEventData['metaEvent']['code'] = "modify" + waitModifyEventData['metaEvent']['code']  # 修改元事件名称
            if waitModify == "name":
                waitModifyEventData = eventRecord().makeupEventData()
                waitModifyEventData['metaEvent']['name'] = "modify" + waitModifyEventData['metaEvent']['name']  # 修改元事件显示名
            if waitModify == "typeId":
                waitModifyEventData = eventRecord().makeupEventData()
                # waitModifyEventData['metaEvent']['typeId'] = allEventType[0]['id']  # 修改元事件分类ID
            if waitModify == "description":
                waitModifyEventData = eventRecord().makeupEventData()
                waitModifyEventData['metaEvent']['description'] = "modify" + waitModifyEventData['metaEvent'][
                    'description']  # 修改元事件描述
            ModifyEventDataList.append(waitModifyEventData)
        for ModifyEventData in ModifyEventDataList:
            name = waitModifyList[ModifyEventDataList.index(ModifyEventData)]
            utils().putOrDelRequest("PUT",url_part,Content_type="json", data=ModifyEventData, Token=self.Token)
            eventRecord().test_05_metaevent()
            if eventContent['metaEvent']['version'] > 1.0:
                print("元事件编辑信息：基本信息"+name+"版本修改--错误，实际不应该被修改")
            else:
                print("元事件编辑信息：基本信息"+name+"版本未变，修改正确")

    def test_0602_metaevent(self):
        '''
        编辑元事件
        2.修改元事件关键词(新增关键词/删除关键词/删除一行关键词)，版本号+0.1
        '''
        url_part = "/dmp-lt/metaevent"
        waitList = ["insert", "delete", "deleteLine"]
        for waitmodifyKeywords in waitList:
            if waitmodifyKeywords == "insert":
                waitModifyEventData = eventRecord().makeupEventData()
                waitModifyEventData['metaEventKeywords'][0]['wordGroup'] = "短信,验证码,测试新增关键词"
            elif waitmodifyKeywords == "delete":
                waitModifyEventData = eventRecord().makeupEventData()
                waitModifyEventData['metaEventKeywords'][1]['wordGroup'] = "短信"
            elif waitmodifyKeywords == "deleteLine":
                waitModifyEventData = eventRecord().makeupEventData()
                waitModifyEventData['metaEventKeywords'] = [waitModifyEventData['metaEventKeywords'][0]]#不保留第二个
            utils().putOrDelRequest("PUT",url_part,Content_type="json", data=waitModifyEventData, Token=self.Token)
            eventRecord().test_05_metaevent()
            if event['version'] > 1.0:
                print("元事件编辑信息：元事件关键词"+waitmodifyKeywords+"版本+0.1，修改正确")
            else:
                print("元事件编辑信息：元事件关键词"+waitmodifyKeywords+"版本未变，修改错误")

    def test_0603_metaevent(self):
        '''
        编辑元事件
        2.修改元事件属性(属性名/属性显示名/数据类型/删除属性/新增属性)，版本号+0.1
        '''
        url_part = "/dmp-lt/metaevent"
        waitList = ["code", "name", "propertyType", "delete", "insert"]
        for Properties in waitList:
            if Properties == "code":
                waitModifyEventData = eventRecord().makeupEventData()
                waitModifyEventData['metaEventProperties'][0]['code'] = "modify"+waitModifyEventData['metaEventProperties'][0]['code']
            elif Properties == "name":
                waitModifyEventData = eventRecord().makeupEventData()
                waitModifyEventData['metaEventProperties'][0]['name'] = "modify"+waitModifyEventData['metaEventProperties'][0]['name']
            elif Properties == "propertyType":
                waitModifyEventData = eventRecord().makeupEventData()
                propertyType = int(waitModifyEventData['metaEventProperties'][0]['propertyType'])
                if propertyType < 4:
                    waitModifyEventData['metaEventProperties'][0]['propertyType'] = str(propertyType + 1)
            elif Properties == "delete":
                waitModifyEventData = eventRecord().makeupEventData()
                removeContent = waitModifyEventData['metaEventProperties'][0]
                removeContent.clear();
                waitModifyEventData['metaEventProperties'] = [waitModifyEventData['metaEventProperties'].pop()]
            elif Properties == "insert":
                waitModifyEventData = eventRecord().makeupEventData()
                PropertiesData = {
                    "code": "M",
                    "name": "M",
                    "propertyType": str(1),
                    "sortNumber": str(0)
                }
                waitModifyEventData['metaEventProperties'].append(PropertiesData)
            utils().putOrDelRequest("PUT",url_part,Content_type="json", data=waitModifyEventData, Token=self.Token)
            eventRecord().test_05_metaevent()
            if eventContent['metaEvent']['version'] > 1.0:
                print("元事件编辑信息：元事件属性"+Properties+"版本+0.1，修改正确")
            else:
                print("元事件编辑信息：元事件属性"+Properties+"版本未变，修改错误")

    def test_0701_delmetaevent(self):
        '''
        删除元事件-情景说明
        一：元事件在当天创建的，可以删除
        '''
        url_part = "/dmp-lt/metaevent/" + str(event['id'])
        print("元事件在当天创建的，删除ID为"+str(event['id'])+"的元事件，删除成功")
        utils().putOrDelRequest("DELETE", url_part, Token=self.Token)

    def test_0702_delmetaevent(self):
        '''
        删除元事件-情景说明
        一：元事件非当天创建的，hive中存在对应的元事件记录不可删除
        '''
        url_part = "/dmp-lt/metaevent/" + str(self.usedEventId)
        print("元事件非当天创建的,删除ID为"+str(self.usedEventId)+"的元事件,删除提示：元事件下存在数据不能被删除")
        utils().putOrDelRequest("DELETE", url_part, Token=self.Token)

    def test_0801_delmetaeventType(self):
        '''
        删除元事件分类-情景说明
        一：分类下不存在元事件，删除成功
        '''
        url_part = "/dmp-lt/metaeventtype/" + str(event['typeId'])
        print("元事件分类下不存在元事件,删除分类ID为"+str(event['typeId'])+"的元事件,删除成功")
        utils().putOrDelRequest("DELETE", url_part, Token=self.Token)

    def test_0802_delmetaeventType(self):
        '''
        删除元事件分类-情景说明
        一：分类下存在元事件，删除失败
        '''
        typeId = 18
        url_part = "/dmp-lt/metaeventtype/" + str(self.usedTypeId)
        print("元事件分类下存在元事件,删除分类ID为"+str(typeId)+"的元事件,删除提示：元事件类型下存在元事件不能删除")
        utils().putOrDelRequest("DELETE", url_part, Token=self.Token)



    def makeupEventData(self):
        data = {
                  "metaEvent": {
                    "code": event['code'],
                    "createTime": event['createTime'],
                    "deleteFlag": event['deleteFlag'],
                    "description": eventContent['metaEvent']['description'],
                    "id": event['id'],
                    "keywordRelation": event['keywordRelation'],
                    "name": event['name'],
                    "projectId": event['projectId'],
                    "typeId": event['typeId'],
                    "updateTime": str(self.nowtime),
                    "version": event['version']
                  },
                  "metaEventKeywords": eventContent['metaEventKeywords'],
                  "metaEventProperties": eventContent['metaEventProperties']
                }
        return data

    def getSqlResult(self):
        '''获取最新事件信息和属性信息'''
        query_param = ['%%%s%%' % 'test']
        eventsql = "SELECT name FROM dmp_meta_event where name like %s order by id asc;"
        eventpropertysql = "SELECT name FROM dmp_meta_event_property where name like %s order by id asc;"
        eventResult = MyDB().executeSQL(eventsql, query_param, database=self.database)
        eventpropertyResult = MyDB().executeSQL(eventpropertysql, query_param, database=self.database)
        if eventResult:
            event = eventResult.split("test")
            if event[1] == "":
                eventnum = "testa"
            else:
                eventnum = "b"
        else:
            eventnum = "testc"
        eventCode = eventResult + eventnum
        eventName = eventResult + eventnum
        if eventpropertyResult:
            propertyName = eventpropertyResult.split("test")
            if propertyName[1] == "":
                propertynum = "testa"
            else:
                propertynum = "b"
        else:
            propertynum = "testc"
        sqlResult = [eventCode, eventName, propertynum]
        return sqlResult

if __name__ == "__main__":

    unittest.main()
    # 流程说明
    # 流程结束
