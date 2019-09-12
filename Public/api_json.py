#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import requests
from pprint import pprint
import os

a = requests.get('http://api.317hu.com/rest/httpMock/interface/11')
# print(resopnse.text)


dict_json = json.loads(a.text)
# print(dict_json)
list_a = []
# print (dict_json.get('interfaceCategoryEntities')[0].get('interfaceHttpEntities')[0].get('description'))

for i in dict_json.get('interfaceCategoryEntities'):
    # print(i)
    # print('\n*************************************************************************')
    # print(i.get('interfaceCategoryName'))
    # print('*************************************************************************\n')

    if i.get('interfaceHttpEntities')==None:
        print(i.get('interfaceCategoryName'))
        print("interfaceCategoryEntities 下没有 interfaceHttpEntities")
    else:
        for j in i.get('interfaceHttpEntities'):
            # print('-----------------------------------------------------------------------------------')
            # print(j.get('name'))

            #### dic_ditiel存放一个接口的相关信息 ####
            dic_ditiel = {}
            dic_ditiel.update({'name': j.get('name')})  # 接口名称
            dic_ditiel.update({'method': j.get('method')})  # 接口请求方式
            dic_ditiel.update({'address': j.get('address')})  # 接口地址

            '''获取接口请求参数'''
            if j.get('interfaceParamEntities') == None:
                pass
            else:
                dict_param = {}
                for k in j.get('interfaceParamEntities'):
                    # print(k.get('example'))
                    # 请求参数名称、示例构成字典dict_parm
                    dict_param.update({k.get('paramName'): k.get('example')})
                dic_ditiel.update({'Params': dict_param})  # 接口请求参数

            '''获取接口头部'''
            if j.get('interfaceParamHeaderEntities') == None:
                pass
            else:
                dict_header = {}
                for l in j.get('interfaceParamHeaderEntities'):
                    # print(l.get('exampleHeader'))
                    dict_header.update({l.get('paramNameHeader'): l.get('exampleHeader')})
                dic_ditiel.update({'Header': dict_header})  # 接口头部

            '''获取返回状态'''
            if j.get('interfaceParamResponseEntities') == None:
                pass
            else:
                dict_Response = {}
                for m in j.get('interfaceParamResponseEntities'):
                    dict_Response.update({m.get('paramNameResponse'): m.get('exampleResponse')})
                dic_ditiel.update({'Response': dict_Response})  # 接口Response

            '''获取返回结果'''
            if j.get('interfaceResultEntities') == None:
                pass
            else:
                n = j.get('interfaceResultEntities')[0]
                dic_ditiel.update({'Result': n.get('exampleContent')})  # 接口Result
            list_a.append(dic_ditiel)




'''lis_a每的每个元素为一个接口的相关参数，以字典的形式保存'''
for a in list_a:
    ''' a has key :
    'name'>>>接口名称,
    'method'>>>>接口请求方式,
    'address'>>>>接口地址,
    'Params'>>>>接口请求参数,
    'Herder'>>>>接口头部,'Response'>>>> 接口Response,
    'Result'>>>> 接口Resultt '''
    print(a)
    print('name>>>>')
    print(a.get('name'))
    # print('Params>>>>')
    # print(a.get('Params'))
    # print('Header>>>>')
    # print(a.get('Header'))
    # print('Response>>>>')
    # print(a.get('Response'))
    # print('Result>>>>')
    # print(a.get('Result'))
    print('-------------------------------------------------------------------------------------\n')
