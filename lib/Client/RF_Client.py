'''
=======================================================================
                        RF Client
=======================================================================
'''
import logging
import visa
from Config.RamaConfig import Config
from Utility.Logger.RamaLogger import RamaLogger

class RF_Client:

    def __init__(self, host, port, timeout=2):
        self.logger = RamaLogger().getLogger()
        self.host = host
        self.port = port
        self.session = visa.ResourceManager('@py')
        self.Connect(timeout * 1000)  # second to millisecond

    def Connect(self, timeout):
        '''Connect to target device.'''
        self.instr = self.session.open_resource("TCPIP::%s::%s::SOCKET"
                                                % (self.host, str(self.port)),
                                                read_termination='\n',
                                                write_termination='\n')
        self.instr.timeout = timeout
        self.logger.info("Already connect to %s:%s" % (self.host, self.port))

    def Disconnect(self):
        '''Disconnect to target device.'''
        self.instr.close()
