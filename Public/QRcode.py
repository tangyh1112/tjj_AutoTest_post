# !/usr/bin/python
# encoding:utf-8

import requests

def QRcode_read(qrurl):
    url = "http://jiema.wwei.cn/url-jiema.html"
    data = {}
    data.update({'jiema_url': qrurl})
    data.update({'token': '7a2ad53317d023abcb8ef755f9fc6e2cd05a8af7'})
    response = requests.post(url, data=data).json()
    return response['data']


if __name__ == '__main__':
    qrurl = 'https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=gQHx8DwAAAAAAAAAAS5odHRwOi8vd2VpeGluLnFxLmNvbS9xLzAyWDJkTTk2RmdkNTExbzRMWDFxMUQAAgQEIlRaAwQAjScA'
    print(QRcode_read(qrurl))
