import requests
import readConfig as readConfig
import Public.Log  as log
import logging

localReadConfig = readConfig.ReadConfig()


class ConfigHttpsit:
    def __init__(self):
        global port, timeout, hostsit
        hostsit = localReadConfig.get_http("baseurlsit")
        port = localReadConfig.get_http("port")
        timeout = localReadConfig.get_http("timeout")
        self.log = log.MyLog.get_log()
        self.logger =   self.log.logger   #logging.getLogger()
        print(3)
        print(self.logger)
        print(4)
        self.headers = {}
        self.params = {}
        self.data = {}
        self.url = None
        self.files = {}

    def set_url(self, url):
        self.url = hostnursetrain + url

    def set_url_sit(self, url):
        self.url = hostsit + url

    def set_headers(self, header):
        self.headers = header

    def set_params(self, param):
        self.params = param

    def set_data(self, data):
        self.data = data

    def set_files(self, file):
        self.files = file

    def get(self):
        try:
            response = requests.get(self.url, params=self.params, headers=self.headers, timeout=float(timeout))
            # response.raise_for_status()
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

    # defined http post method
    def post(self):
        try:
            response = requests.post(self.url, headers=self.headers, data=self.data, files=self.files,
                                     timeout=float(timeout))
            # response.raise_for_status()
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

if __name__ =='__main__':
    sit = ConfigHttpsit()



    
