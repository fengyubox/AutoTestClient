'''
=======================================================================
                        STP Client
=======================================================================
A child class which is a specific class for STP Server extends all of
attributes and SendCmd function. Authentication before send STP Command
to operate STP Server by TestPC.
=======================================================================
'''
import logging
from Client.ParentClient import Client
from CommandSet.STP.GetAuth import Authentication
from Decorator.Retry import retry
from Config.RamaConfig import Config
from Utility.Logger.RamaLogger import RamaLogger

class STPClient(Client):
    def __init__(self, ConnectionType):
        self.logger = RamaLogger().getLogger()
        super().__init__(ConnectionType)
        self.Auth()

    @retry(Exception, reconnect_when_error=True)
    def SendCmd(self, CmdObj, **kwargs):
        return super().SendCmd(CmdObj, **kwargs)

    def Connect(self):
        super().Connect()
        self.Auth()

    def Auth(self):
        Auth = Authentication()
        self.ConnectionType.Send(Auth.PackCommand())
