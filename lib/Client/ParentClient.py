'''
=======================================================================
                        ParentClient
=======================================================================
A parent class to implement common TestPC client to operate target
device by connectiontype which is an input when creating client object.
=======================================================================
'''
import logging
from struct import calcsize
from Config.RamaConfig import Config
from Utility.Logger.RamaLogger import RamaLogger

class Client:

    def __init__(self, ConnectionType):
        self.logger = RamaLogger().getLogger()
        self.ConnectionType = ConnectionType

    def SendCmd(self, CmdObj, **kwargs):
        self.ConnectionType.Send(CmdObj.PackCommand())

        if 'receiveAfterSend' not in kwargs:
            kwargs['receiveAfterSend'] = True

        if kwargs['receiveAfterSend']:
            ResponseLength = (calcsize(CmdObj.ResponseHeaderFormat) +
                            calcsize(CmdObj.ResponsePayloadFormat))
            Response = self.ConnectionType.Receive(ResponseLength)
            CmdObj.UnpackResponse(Response)
            rc, resMsg = CmdObj.ReturnCheck()
            CmdObj.STDOut()
            return rc, resMsg

    def Connect(self):
        self.ConnectionType.Connect()

    def Disconnect(self):
        self.ConnectionType.Disconnect()
