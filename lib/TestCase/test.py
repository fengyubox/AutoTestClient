import logging
import sys
import os
import abc
# Import Rama library
sys.path.insert(0, os.path.join(os.path.join(
    os.path.dirname(__file__), os.pardir, os.pardir), 'lib'))
from ConnectionType.ssh import SSHConnection
from argparse import ArgumentParser
from Config.RamaConfig import Config
from Utility.Logger.RamaLogger import RamaLogger

class BaseTestCase(metaclass=abc.ABCMeta):

    isConnectToDut = True

    def __init__(self):
        self.initParser()
        self.logger = RamaLogger().getLogger()

    def initParser(self):
        self.parser = ArgumentParser()
        self.loadCommonArgs()
        self.loadCriteria()
        self.args = self.parser.parse_args()

    def loadCommonArgs(self):
        self.parser.add_argument("-v", "--verbose", action='store_true',
                                 help="verbose mode")

    def loadCriteria(self):
        pass

    def setUp(self):
        # Create socket connection
        self.logger.info('------------------ Test Start ------------------')
        if self.isConnectToDut:
            self.connectToDut()

    def test(self):
        self.setUp()
        result = self._runTest()
        self.tearDown()
        return result

    def connectToDut(self):
        ip = Config.get("DUT", "IP").replace("'", "")
        port = Config.getint('DUT', 'PORT')
        conn = SocketConnection(ip, port)
        # conn = SerialConnection()
        self.stpClient = STPClient(conn)

    @abc.abstractmethod
    def _runTest(self):
        pass

    def tearDown(self):
        if hasattr(self, "stpClient") and self.stpClient is not None:
            self.stpClient.Disconnect()
        self.logger.info('----------------- Test Finish! -----------------')
