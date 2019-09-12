#!C:\Program Files\Python36 python
# -*- coding: utf-8 -*-

import readConfig as readConfig
import unittest
import sys
import os
case_path = sys.path[0]
localReadConfig = readConfig.ReadConfig()
class eventRecord(unittest.TestCase):

    def test(self):
        '''批量生成手机号'''
        name = "phone.txt"
        if os.path.exists(name):
            os.remove(name)
        with open(name, "w") as file:
            for i in range(13330010499, 13330060499):
                file.write(str(i) + "\n")
        file.close()

