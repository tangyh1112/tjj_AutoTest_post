# coding = utf-8
import json,os
import logging


class cmp_result:
#    judge = False
#    temp_data = dict()
#    import_param = dict()

    @staticmethod
#    def cmp(fix_data, return_data):
#        """
#        函数递归，判断fix字典是否和return字典的部分内容一样
#        :param fix_data: 正确的字典数据
#        :param return_data: 返回的自动数据
#        :return:
#        """
#        for n1 in fix_data:
#            if isinstance(fix_data[n1],dict):  # 如果n1是字典数据，进入递归判断
#                if not SHTestCase.cmp(fix_data[n1],return_data.get(n1)):
#                    return False
#            elif isinstance(fix_data[n1], list):  # 如果n1是列表数据，进入递归判断
#                for num, n3 in enumerate(fix_data[n1]):
#                    for num1, n4 in enumerate(return_data[n1]):
#                        if not return_data[n1]:
#                            raise '{}返回数据为空'.format(n1)
#                        if SHTestCase.cmp(fix_data[n1][num],return_data[n1][num1]):
#                            SHTestCase.judge = True  # 当存在相同数据，judge为真，结束该轮循环；否则，由于递归，judge自动为假，
#                            break
#                    if not SHTestCase.judge:  # 结束子循环后，judge没有为真，则可以判断数据不一致，返回False
#                        return False
#            else:
#                if fix_data[n1] == return_data.get(n1):  # 对非字典和列表的数据，进入判断
#                    continue
#                else:
#                    SHTestCase.temp_data['error_data'] = '{}:{} , {}:{}'.format(n1, fix_data[n1], n1,
#                                                                                return_data.get(n1))
#                    return False
#        SHTestCase.judge = False
#        SHTestCase.temp_data['error_data'] = ''
#        return True
    def cmp(src_data, dst_data):
        if isinstance(src_data, dict):
            """若为dict格式"""
            for key in dst_data:
                if key not in src_data:
                    logging.info("接口返回结果%s\n缺少中了这个key值:%s" % (src_data, key))
                    raise Exception("接口返回结果%s\n中多了这个key值:%s" % (src_data, key))
            for key in src_data:
                if key in dst_data:
                    """递归"""
                    cmp_result.cmp(src_data[key], dst_data[key])

                else:
                    logging.info('接口返回结果%s中\n多出了这个key值:%s' % (src_data, key))
                    raise Exception('接口返回结果%s中\n多出了这个key值:%s' % (src_data, key))

        elif isinstance(src_data, list):
            """若为list格式"""
            if len(src_data) != len(dst_data):
                logging.info("list len not : '{}' != '{}'".format(len(src_data), len(dst_data)))
                raise Exception("接口返回结果%s\nExcel数据%s 长度不一致" % (src_data, dst_data))

            for src_list, dst_list in zip(src_data, dst_data):
                cmp_result.cmp(src_list, dst_list)

        else:
            if str(src_data) != str(dst_data):
                logging.info('接口返回response：%s >>>>>>>>>>>>>>>>>>>>>>>>>>Excel的result：%s ' % (src_data, dst_data))

    @staticmethod
    def result_json(result):
        return json.loads(result.content.decode())  # 将json数据解析为字典数据

    @staticmethod
    def result_assert(fix_data, return_data):
        cmp_result.judge = False
        if isinstance(return_data, list):
            return_data = return_data[0]
        assert cmp_result.cmp(fix_data, return_data), '错误信息段:{}\n 正确数据:{}\n 返回数据:{}'.format(
            cmp_result.temp_data['error_data'], fix_data, return_data)

    @staticmethod
    def easy_assert(result):
        """ 判断返回数据不为空，或者返回数据中data的值不为空

        """
        if isinstance(result, list):
            if result[0].get('data'):
                print('用例通过')
                return
            elif result[0].get('data') == None:
                if result:
                    print('用例通过')
                    return
                else:
                    assert '返回数据为空'
            else:
                assert '返回数据中，data的数据为空'
        if result.get('data'):
            print('用例通过')
        elif result.get('data') == None:
            if result:
                print('用例通过')
            else:
                assert '返回数据为空'

        else:
            assert '返回数据中，data的数据为空'

    @staticmethod
    def get_value(result, param):
        """ eg:需要获取值result['1']['2'], 则param:['1','2']
        
        :param result: http返回结果
        :param param: 需要获取参数的路径list
        """
        if isinstance(result, list):
            result = result[param.pop(0)]
        num = len(param)
        if num == 1:
            return result[param[0]]
        else:
            return cmp_result.get_value(result[param.pop(0)], param)

    @staticmethod
    def dict_value(param):
        param_value = sorted(param.items(), key=lambda param: param[0])
        listvalue = []
        for index in range(len(param_value)):
            strm = '='
            paramkey = param_value[index][0]
            paramvalue = param_value[index][1]
            paramcon = str(paramkey).lower() + str(strm) + str(paramvalue)
            listvalue.append(paramcon)
        paramcontent = "&".join(listvalue)
        return paramcontent

    def get_param(self, p):
        """ p['_use']内容，若为真，则提取p['_use'][x]的值，所对应的的临时字典SHTestCase.temp_data的x的值的健（说的有的混乱~~）
        
        :param p: 
        """
        if p['_use']:
            for n in p['_use'].keys():
                print(n)
                self.import_param[n] = self.temp_data[p['_use'][n]]
            self.import_param.update(p['_param'])
            return self.import_param
        else:
            return p['_param']

    def set_param(self, result, p):
        """ 若p['_get']，则收集返回数据的某些参数
        
        :param result: http返回的数据
        """
        if p['_get']:
            for n in p['_get'].keys():
                self.temp_data[n] = self.get_value(result, p['_get'][n])
        self.import_param.clear()  # 每次请求结束后，clear该字典，确保下个请求时，该字典为空，防止参数继承于上次请求

    def case_logic(self, _data, deep_contrast=True):
        """ 接口用例执行逻辑模板

        """
        param = self.get_param(_data)   # 获取参数
        u = getattr(self, _data['_user'])   # 设置指定用户
        self.re = getattr(u, _data['re'])   # 设置请求方式
        url = '{}{}'.format(self.ip, _data['_api'])
        result = self.re(url, param)
        result = self.result_json(result)
        self.set_param(result, _data)   # 提取需要保存的返回数据
        if deep_contrast:
            self.result_assert(_data['result'], result)     # 对返回数据做比较
        else:
            self.easy_assert(result)
    @staticmethod
    def cmp_str(orignstr,cstr):
        if cstr in orignstr:
            print("code")
            passOrFail = 0
        else:
            raise ValueError
            passOrFail = 1
        return passOrFail

    @staticmethod
    def GetFileNameAndExt(filename):
        (shotname, extension) = os.path.splitext(filename)
        return shotname, extension



