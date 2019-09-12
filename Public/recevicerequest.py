#!/usr/bin/env python
# -*- coding: utf-8 -*
import types
import urllib.request
import json

# 利用urllib2获取网络数据
def registerUrl():
    try:
        url = "http://api.317hu.com/rest/httpMock/interface/11"
        data = urllib.request.urlopen(url).read().decode('utf-8')
        return data
    except Exception:
        print("false")

        # 写入文件


def jsonFile(fileData):
    file = open("d:\\json.txt", "w")
    file.write(str(fileData))
    file.close()

## 解析从网络上获取的JSON数据
def praserJsonFile(jsonData):
#    jsonData.decode("utf-8")
    value = json.loads(jsonData)#
    rootlist = value.keys()
#    print (rootlist)
##    print duan
    for rootkey in rootlist:
        if rootkey == "interfaceCategoryEntities":

            subvalue = value[rootkey]
            lst = [item[key] for item in subvalue for key in item ]


if __name__ == "__main__":

    data = registerUrl()
    jsonFile(data)
#
    praserJsonFile(data)
#