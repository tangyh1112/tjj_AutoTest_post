#!/usr/bin/env python
# -*- coding: utf-8 -*-
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import readConfig as readConfig
import logging

localReadConfig = readConfig.ReadConfig()


class Email:
    def __init__(self):
        global host, user, password, port, sender, title, content
        host = localReadConfig.get_email("mail_host")
        user = localReadConfig.get_email("mail_user")
        password = localReadConfig.get_email("mail_pass")
        port = localReadConfig.get_email("mail_port")
        sender = localReadConfig.get_email("sender")
        title = localReadConfig.get_email("subject")
        content = localReadConfig.get_email("content")
        self.ON_OFF = localReadConfig.get_email("on_off")
        self.value = localReadConfig.get_email("receiver")
        self.receiver_byself = localReadConfig.get_email("receiver_byself")
        self.receiver = []
        for n in str(self.value).split("/"):
            self.receiver.append(n)
        date_time = time.strftime('%Y-%m-%d_%H_%M', time.localtime(time.time()))
        self.subject = title + " " + date_time

    def create_emali(self, report):
        # 构造邮件头部
        msg = MIMEMultipart('related')
        msg['Subject'] = self.subject
        msg['From'] = sender
        msg['To'] = ";".join(self.receiver)

        # 构造附件 如果要带报告，打开即可
        # try:
        #     logging.info('读取测试报告并添加到邮件附件中....')
        #     att = MIMEText(open(report, 'rb').read(), 'base64', 'utf-8')
        # except(NameError, IOError, ValueError) as e:
        #     logging.error(e)
        # else:
        #     att["ContentType"] = 'application/octet-stream'
        #     att['Content-Disposition'] = 'attachment; filename = "API_AutoTest_Report.html"'
        #     msg.attach(att)


        # 添加邮件正文内容
        msg_text = MIMEText(content, 'plain', 'utf-8')
        msg.attach(msg_text)
        return msg

    def send_email(self, report):
        if int(self.ON_OFF) == 1:
            msg = self.create_emali(report)
            try:
                smtp = smtplib.SMTP()
                smtp.connect(host)
                smtp.login(user, password)
                smtp.sendmail(sender, self.receiver, msg.as_string())
                smtp.quit()
                # print("success")
                logging.info("邮件已发送成功")

            except Exception as ex:
                logging.error(str(ex))
        elif int(self.ON_OFF) == 0:
            logging.info("不发送邮件 ")
        else:
            logging.error("Config Email on-off 设置无效，1-发送邮件；2-不发送")


    def send_email_bySelf(self, report):
        #只发给测试部  receiver_byself
        if int(self.ON_OFF) == 1:
            msg = self.create_emali(report)
            try:
                smtp = smtplib.SMTP()
                smtp.connect(host)
                smtp.login(user, password)
                smtp.sendmail(sender, str(self.receiver_byself), msg.as_string())
                smtp.quit()
                logging.info("邮件已发送成功")
            except Exception as ex:
                logging.error(str(ex))
        elif int(self.ON_OFF) == 0:
            logging.info("不发送邮件 ")
        else:
            logging.error("Config Email on-off 设置无效，1-发送邮件；2-不发送")
