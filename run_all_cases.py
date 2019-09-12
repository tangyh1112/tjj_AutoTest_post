#!/usr/bin/env python
# -*- coding: utf-8 -*-


from Public.Log import Log
from Public.CaseStrategy import CaseStrategy
from Public.RunCases import RunCases
from Public.configEmail import Email
import sys

if __name__ == '__main__':
    Run = RunCases()
    # 创建报告地址
    report_path = Run.create_path()
    report_name = report_path + '/' + 'Run_All_TestReport.html'
    # 创建Log
    log = Log()
    log.set_logger(report_path)
    # 创建用例
    cs = CaseStrategy()
    cases = cs.collect_cases(suite=True)
    Run.run(report_name, cases)
    # 发送邮件
    # email = Email()
    # email.send_email(report_name)#这里待的报告，是否使用看的是configEmail,如果要使用报告，放开相应注释即可





