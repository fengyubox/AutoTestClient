import serial
import logging
import sys
import time
from .IConnectionType import ConnectionType
from functools import wraps
from Decorator.Retry import retry
from Config.RamaConfig import Config
from Utility.Logger.RamaLogger import RamaLogger


class SerialConnection(ConnectionType):
    def __init__(self, device='/dev/ttyACM0', baudRate=115200, recvTimeout=20):
        self.logger = RamaLogger().getLogger()
        self.device = device
        self.baudRate = baudRate
        self.recvTimeout = recvTimeout
        self.Connect()

    def Connect(self):
        self.logger.info("Connecting to %s" % self.device)
        self.server = serial.Serial(self.device, self.baudRate, timeout=self.recvTimeout)
        self.logger.info("Already connect to %s" % self.device)

    def Send(self, cmd):
        self.logger.debug('Commnad: ' + str(cmd))
        self.server.write(cmd)

    def Receive(self, response_length):
        response = self.server.read(response_length)
        return response

    def Disconnect(self):
        '''Disconnect to target device.'''
        self.server.close()
        self.server = None
        self.logger.info('Serial connection is closed.')




