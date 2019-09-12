# -*- coding: utf-8 -*-
import os
import codecs
import configparser


proDir = os.path.split(os.path.realpath(__file__))[0]
#将path分割成路径名和文件名123
configPath = os.path.join(proDir, "config.ini")
#将多个路径组合后返回

class ReadConfig:

    def __init__(self):
        self.cf = configparser.ConfigParser()
        self.cf.read(configPath, encoding='UTF-8')

    def get_email(self, name):
        value = self.cf.get("EMAIL", name)
        return value

    def get_http(self, name):
        value = self.cf.get("HTTP", name)
        return value

    def get_db(self, name):
        value = self.cf.get("DATABASE", name)
        return value


# if __name__ == "__main__":
#
#     ReadConfig()