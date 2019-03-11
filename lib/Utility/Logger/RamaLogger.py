import logging
import time
import os
import sys

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class RamaLogger(metaclass=Singleton):

    def __init__(self):

        self.logger = logging.getLogger('RamaLogger')
        self.logger.setLevel(logging.DEBUG)

        self.__stepIndex = 0

        logFolderName = 'log'
        baseDir = os.path.dirname(sys.argv[0])

        log_dir = os.path.join(baseDir, logFolderName)
        
        # check if log folder is exist
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        logFilename = os.path.splitext(os.path.basename(sys.argv[0]))[0]
        logPath = os.path.join(log_dir, '%s.log' % logFilename)
        self.logname = os.path.abspath(logPath)

        # create logging format
        self.formatter = logging.Formatter('[%(asctime)s] [%(module)13s] [%(levelname)5s]  %(message)s')

        fh = logging.FileHandler(self.logname, 'w')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(self.formatter)

        # create a console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(self.formatter)

        if not self.logger.handlers:
            self.logger.addHandler(ch)
            self.logger.addHandler(fh)
        
    def resetStepIndex(self):
        self.__stepIndex = 0

    def __log(self, level, message):

        if level == 'info':
            self.logger.info(message)
        elif level == 'step':
            self.__stepIndex += 1
            self.logger.info("%d. %s" % (self.__stepIndex, message))
        elif level == 'debug':
            self.logger.debug(message)
        elif level == 'warning':
            self.logger.warning(message)
        elif level == 'error':
            self.logger.error(message)

    def debug(self, message):
        self.__log('debug', message)

    def info(self, message):
        self.__log('info', message)

    def warning(self, message):
        self.__log('warning', message)
    
    def error(self, message):
        self.__log('error', message)

    def error_code(self, errorcode):
        self.__log('error', "RAMA_ERRORCODE=" + errorcode)

    def error_msg(self, message):
        self.__log('error', "RAMA_ERRORMSG=" + message)
    
    def step(self, message):
        self.__log('step', message)
    
    def getLogger(self):
        return self.logger
