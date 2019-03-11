'''
=======================================================================
                        RF Client
=======================================================================
'''
import visa
from Utility.Logger.RamaLogger import RamaLogger


class DC_Client:

    def __init__(self, resource, timeout=2):
        self.logger = RamaLogger().getLogger()
        self.resource = resource
        self.session = visa.ResourceManager('@py')
        self.Connect(timeout * 1000)  # second to millisecond

    def Connect(self, timeout):
        '''Connect to target device.'''
        try:
            self.instr = self.session.open_resource(self.resource,
                                                read_termination='\n',
                                                write_termination='\n')
            self.instr.timeout = timeout
            self.logger.info("Already connect to %s" % (self.resource))
        except Exception as e:
            self.logger.error_code('IN10')
            self.logger.error_msg("Connect to {0} failed".format(self.resource))
    def Disconnect(self):
        '''Disconnect to target device.'''
        self.instr.close()
