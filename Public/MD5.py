#!C:\Users\dell\AppData\Local\Programs\Python\Python35 python
# -*- coding: utf-8 -*-
import hashlib
def md5(str):
        m = hashlib.md5()
        m.update(str.encode("utf8"))
        return m.hexdigest()
