#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
import logging
from Public.HTMLTestReportCN import HTMLTestRunner
import shutil
# '''报告增加饼状图'''
# from Public.HTMLTestRunner_PY3 import HTMLTestRunner
# import shutil

class RunCases:
    ''' 创建报告地址 test_report_path '''
    def create_path(self):
        self.test_report_root = './Report'
        if not os.path.exists(self.test_report_root):
            os.mkdir(self.test_report_root)
        date_time = time.strftime('%Y-%m-%d_%H_%M_%S', time.localtime(time.time()))
        self.test_report_path = self.test_report_root + '/' + date_time
        # self.test_report_path = self.test_report_root
        if not os.path.exists(self.test_report_path):
            os.mkdir(self.test_report_path)

        # '''
        # 报告增加饼状图
        # 复制\Public\js\echarts.common.min.js到 test_report_path的js文件夹内
        # '''
        # self.js_path = self.test_report_path + '/'+'js'
        # if not os.path.exists(self.js_path):
        #     os.mkdir(self.js_path)
        # shutil.copy('./js/echarts.common.min.js', self.js_path)
        return self.test_report_path

    def run(self, report_name, cases):
        # try:
        #     with open(report_name, 'wb') as file:
        #         logging.info('开始执行测试')
        #         runner = HTMLTestRunner(stream=file, title='自动化接口测试报告', description='用例执行情况：')
        #         runner.run(cases)
        #         file.close()
        #         logging.info('测试执行成功')
        #         logging.info('测试报告保存路径为： %s' % report_name)
        #         shutil.copyfile(report_name, './Report/TestReport.html')
        #
        # except:
        #     logging.error('HTMLTestRunner running Failed')
        #     raise Exception('HTMLTestRunner running Failed')

        with open(report_name, 'wb') as file:
            logging.info('开始执行测试')
            runner = HTMLTestRunner(stream=file, title='自动化接口测试报告', description='用例执行情况：')
            logging.info('---HTMLTestRunner---')
            runner.run(cases)
            logging.info('---Runcases start---')
            file.close()
            logging.info('测试执行成功')
            logging.info('测试报告保存路径为： %s' % report_name)
            shutil.copyfile(report_name, './Report/TestReport.html')





