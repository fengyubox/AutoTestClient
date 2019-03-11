'''
================================================================
                        SocketConnection
================================================================
The class implement how to communicate with target device by
Socket with IP and Port of target device. There are four
function as below.
Function:
1. Connect():    Open the socket of client to connect to server
                 which is on target device.

2. Send():       Send suitable command which is an input to
                 target device.

3. Receive():    Receive corresponding response from targe device,
                 after sending command. Input a response length
                 to predefine how many bytes for buffer should
                 be reserve.

4. Disconnect(): Close the socket of client to disconnect to
                 server which is on target device.

Input of creating object: IP and Port of target device.
Ex: ConnectionType = SocketConnection("192.168.84.1",7654)
================================================================
'''

import socket
import logging
import sys
import time
from .IConnectionType import ConnectionType
from functools import wraps
from Decorator.Retry import retry
from Config.RamaConfig import Config
from Utility.Logger.RamaLogger import RamaLogger

class SocketConnection(ConnectionType):
    def __init__(self, host, port, recvTimeout=50):
        self.logger = RamaLogger().getLogger()
        self.recvTimeout = recvTimeout
        self.host = host
        self.port = port
        '''OpenSocket'''
        self.Connect()

    @retry(Exception)
    def Connect(self):
        self.logger.info("Connecting to %s:%s" % (self.host,self.port))
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.settimeout(self.recvTimeout)
        self.server.connect((self.host,self.port))
        self.logger.info("Already connect to %s:%s" % (self.host,self.port))

    def Send(self, cmd):
        self.logger.debug('Commnad: ' + str(cmd))
        self.server.sendall(cmd)

    def Receive(self, response_length):
        response = self.server.recv(response_length)
        self.logger.info("Raw Data:")
        self.logger.info(response)
        return response

    def Disconnect(self):
        '''Disconnect to target device.'''
        self.server.close()
        self.server = None
        self.logger.info('Socket is Closed.')




