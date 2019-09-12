#!C:\Users\dell\AppData\Local\Programs\Python\Python35 python
# -*- coding: utf-8 -*-
import sys, os

class Fileoperation:
    # def __init__(self):
        # self.case_path = sys.path[0]
        # self.case_path = os.getcwd()

    def filewrite(self, fpath, filename, writeword):
        filepath = os.path.join(fpath, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(writeword)
            f.close()

    def fileread(self, fpath, filename):
        filepath = os.path.join(fpath, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            try:
                all_the_text = f.read()
            finally:
                f.close()
        return (all_the_text)

# class Fileoperation:
#     def __init__(self):
#         self.case_path = sys.path[0]
#     def filewrite(self,filename,writeword):
#         filepath = os.path.join(self.case_path, filename)
#         with open(filepath, 'w', encoding='utf-8') as f:
#             f.write(writeword)
#             f.close()
#     def fileread(self,filename):
#         filepath = os.path.join(self.case_path,filename)
#         with open(filepath, 'r', encoding='utf-8') as f:
#             try:
#                 all_the_text = f.read()
#             finally:
#                 f.close()
#         return(all_the_text)
