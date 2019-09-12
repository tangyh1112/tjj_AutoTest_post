import logging
import logging.config
import threading
import os

class Log:
    @classmethod
    def set_logger(cls, file):
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        fh = logging.FileHandler(os.path.join(file, "output.log"), mode='w', encoding='UTF-8')
        fh.setLevel(logging.INFO)

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        logger.addHandler(fh)
        logger.addHandler(ch)

        cls.logger = logger

    def d(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def i(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def w(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def c(self, msg, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)

    def e(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    # def __init__(self):
    #     global logPath, resultPath, proDir
    #     proDir = readConfig.proDir
    #     resultPath = os.path.join(proDir, "result")
    #     # create result file if it doesn't exist
    #     if not os.path.exists(resultPath):
    #         os.mkdir(resultPath)
    #     # defined test result file name by localtime
    #     logPath = os.path.join(resultPath, str(datetime.now().strftime("%Y%m%d%H%M%S")))
    #     # create test result file if it doesn't exist
    #     if not os.path.exists(logPath):
    #         os.mkdir(logPath)
    #
    #     # defined logger
    #     self.logger = logging.getLogger()
    #     # defined log level
    #     self.logger.setLevel(logging.INFO)
    #
    #     # defined handler
    #     fh = logging.FileHandler(os.path.join(self.test_report_path, "output.log"), mode='w')
    #     fh.setLevel(logging.DEBUG)
    #     ch = logging.StreamHandler()
    #     ch.setLevel(logging.WARNING)
    #     # defined formatter
    #     formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    #     # defined formatter
    #     fh.setFormatter(formatter)
    #     ch.setFormatter(formatter)
    #     # add handler
    #     self.logger.addHandler(fh)
    #     self.logger.addHandler(ch)

# class MyLog:
#     log = None
#     mutex = threading.Lock()
#
#     def __init__(self):
#         pass
#
#     @staticmethod
#     def get_log():
#
#         if MyLog.log is None:
#             MyLog.mutex.acquire()
#             MyLog.log = Log()
#             MyLog.mutex.release()
#
#         return MyLog.log
