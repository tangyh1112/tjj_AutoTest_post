# -*- coding: utf-8 -*-

import urllib
from urllib import request, error
from urllib.parse import urlparse, parse_qs

from http import cookiejar


class HttpRequest:
    def __init__(self):
        '''
        cookie = cookiejar.CookieJar()
        cookieProc = request.HTTPCookieProcessor( cookie )
        opener = request.build_opener( cookieProc )
        request.install_opener( opener )
        '''
        
        cj = cookiejar.LWPCookieJar()  
        cookie_support = request.HTTPCookieProcessor(cj)
        for item in cj:
            print('Name1 = ' + item.name)
            print('Value2 = ' + item.value)
        opener = request.build_opener(cookie_support, request.HTTPHandler)  
        #proxy_support = request.ProxyHandler({'http':'http://120.193.146.97:843'})
        #opener = request.build_opener(proxy_support, cookie_support, request.HTTPHandler)
        request.install_opener(opener)
        self.req = request
        

    def request(self, url: object, header: object = {}, add: object = {}, datas: object = None) -> object:

        if url == None or url == '': return None
        #url = 'http://www.hyg.com/123php.php'
        if datas and header:
            req = self.req.Request(url, data = datas, headers = header)
        elif datas:
            req = self.req.Request(url, data = datas)
        elif header:
            req = self.req.Request(url, headers = header)
        else:
            req = self.req.Request(url)

        if add:
            for key in add:
                req.add_header(key, add[key])
        
        try:
            fp = self.req.urlopen(req)
            return (fp.getheaders(), fp.read(), fp.geturl())
        except Exception as err:
            print(err)
            return (None, None, None)
        

    def getUrlParm(self, Url, key):
        o = urlparse(Url)
        qs = parse_qs(o.query)
        #print(qs)
        return qs[key][0]
    
