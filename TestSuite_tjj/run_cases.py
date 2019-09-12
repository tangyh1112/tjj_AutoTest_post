#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('..')

import logging
from Public.CaseStrategy import CaseStrategy
from Public.RunCases import RunCases
from Public.configEmail import Email
from Public.Log import Log

if __name__ == '__main__':
    Run = RunCases()
    # 创建报告地址
    report_path = Run.create_path()
    report_name = report_path + '/' + 'TestReport.html'
    # 创建Log
    log = Log()
    log.set_logger(report_path)
    # 创建用例
    cs = CaseStrategy()
    cases = cs.collect_cases(suite=False)
    # 运行测试
    Run.run(report_name, cases)
    # 发送邮件
    # email = Email()
    # email.send_email_bySelf(report_name)




