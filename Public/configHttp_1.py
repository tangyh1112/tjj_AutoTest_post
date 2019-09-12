from Public.Log  import MyLog as Log
import json
import requests
from pprint import pprint
import os
import readConfig as readConfig
localReadConfig = readConfig.ReadConfig()

class ConfigHttp:
    def __init__(self):
        global host
        host = localReadConfig.get_http("baseurl")
    # defined http get method
    def cmp(src_data, dst_data):
        if isinstance(src_data, dict):
            """若为dict格式"""
            for key in dst_data:
                if key not in src_data:
                    print("src不存在这个key")
            for key in src_data:
                if key in dst_data:
                    thiskey = key
                    """递归"""
                    cmp(src_data[key], dst_data[key])
                else:
                    dic[key] = ["dst不存在这个key"]
        elif isinstance(src_data, list):
            """若为list格式"""
            if len(src_data) != len(dst_data):
                print("list len: '{}' != '{}'".format(len(src_data), len(dst_data)))
            for src_list, dst_list in zip(sorted(src_data), sorted(dst_data)):
                """递归"""
                cmp(src_list, dst_list)
        else:
            if str(src_data) != str(dst_data):
                print(src_data)
    def get(self):
        try:
            ConfigHttp.__init__(self)
            Request_Method_1 = "GET"
            Request_Method_2 = "POST"
            result = requests.get('http://api.317hu.com/rest/httpMock/interface/11')
            dict_json = json.loads(result.text)
            list_a = []
            for i in dict_json.get('interfaceCategoryEntities'):
                for j in i.get('interfaceHttpEntities'):
                    Request_Method = j.get("method")
                    dic_ditiel = {}
                    # 接口名称
                    dic_ditiel.update({'name': j.get('name')})
                    # 接口请求方式
                    dic_ditiel.update({'method': j.get('method')})
                    # 接口地址
                    dic_ditiel.update({'address': j.get('address')})
                    if j.get('interfaceParamEntities') == None:
                        pass
                    else:
                        dict_param = {}
                        for k in j.get('interfaceParamEntities'):
                            # print(k.get('example'))
                            # 请求参数名称、示例构成字典dict_parm
                            dict_param.update({k.get('paramName'): k.get('example')})
                        # 接口请求参数
                        dic_ditiel.update({'Params': dict_param})
                    if j.get('interfaceParamHeaderEntities') == None:
                        pass
                    else:
                        dict_header = {}
                        for l in j.get('interfaceParamHeaderEntities'):
                            # print(l.get('exampleHeader'))
                            dict_header.update({l.get('paramNameHeader'): l.get('exampleHeader')})
                        # 接口头部
                        dic_ditiel.update({'Header': dict_header})
                    if j.get('interfaceParamResponseEntities') == None:
                        pass
                    else:
                        dict_Response = {}
                        for m in j.get('interfaceParamResponseEntities'):
                            dict_Response.update({m.get('paramNameResponse'): m.get('exampleResponse')})
                        # 接口Response
                        dic_ditiel.update({'Response': dict_Response})

                    '''获取返回结果'''
                    if j.get('interfaceResultEntities') == None:
                        pass
                    else:
                        n = j.get('interfaceResultEntities')[0]
                        dic_ditiel.update({'Result': n.get('exampleContent')})  # 接口Result
                    list_a.append(dic_ditiel)
                    for a in list_a:
                        ''' a has key :
                        'name'>>>接口名称,
                        'method'>>>>接口请求方式,
                        'address'>>>>接口地址,
                        'Params'>>>>接口请求参数,
                        'Herder'>>>>接口头部,'Response'>>>> 接口Response,
                        'Result'>>>> 接口Resultt '''
                        self.url = host + a.get('address')
                        self.data = a.get('Params')
                        self.headers = a.get('Header')
                        Response = a.get('Response')
                        Result = a.get('Result')

                    if Request_Method == Request_Method_1:
                        response = requests.get(self.url,data=self.data,headers = self.headers)
                        response.raise_for_status()

                    elif Request_Method == Request_Method_2:
                        response = requests.post(self.url,data=self.data,headers = self.headers)
                        response.raise_for_status()
                    else:
                        print(self.url)

                    ConfigHttp.cmp(response.text,Result)

#                return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

#    # defined http post method
#    def post(self):
#        try:
#            ConfigHttp.__init__(self)
#            for num in range(0, length1-1):
#                self.headers = post[num+1][1]
#                self.params = post[num+1][2]
#                self.url = host + post[num+1][3]
#            response = requests.post(self.url, headers=self.headers, data=self.data,timeout=float(timeout))
#            response.raise_for_status()
#            return response
#        except TimeoutError:
#            self.logger.error("Time out!")
#            return None
