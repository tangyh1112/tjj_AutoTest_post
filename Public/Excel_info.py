#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xlrd
import sys
import logging
import os


class excel_info(object):
    def __init__(self, name="testinfo.xls", xls_path=''):
        logging.info(sys.path[0])
        if os.path.basename(sys.path[0]) == "TestCase":
            self.path = xls_path+"/" + name
        else:
            self.path = xls_path+"/TestCase"+'/' + name
        logging.info(self.path)
        logging.info("读取接口信息从Excel:%s  " % self.path)
        try:
            self.xl = xlrd.open_workbook(self.path)
        except (IOError, ImportError, ValueError, NameError) as e:
            logging.error(e)
            raise Exception(e)

    def flottostr(self, val):
        if isinstance(val, float):
            val = str(int(val))
        return val

    def get_xlsinfo(self):
        listkey = ['headers', 'params', 'url', 'result']
        api_dic = {}
        for row in range(1, self.sheet.nrows):
            info = [self.flottostr(val) for val in self.sheet.row_values(row)]
            api_key = info[0]
            info.pop(0)
            tmp = zip(listkey, info)
            api_dic.update({api_key: dict(tmp)})

        return api_dic

    def get_sheetinfo_by_name(self, name):
        self.sheet = self.xl.sheet_by_name(name)
        return self.get_xlsinfo()

    def get_sheetinfo_by_index(self, index):
        self.sheet = self.xl.sheet_by_index(index)
        return self.get_xlsinfo()

# if __name__ == '__main__':
#     xls = excel_info('.\login.xls')
#     info = xls.get_sheetinfo_by_index(0)
#     print(info)
#     info = xls.get_sheetinfo_by_name('Sheet1')
#     print(info)
