from .Group import ServerGroup
from struct import pack, unpack_from, calcsize


class GetHandlerList(ServerGroup):
    def __init__(self):
        super().__init__()
        self.SendCmdid = 2
        self.SendPaylen = 0
        self.ResponsePayloadFormat = "<I192s"
        self.numHandlers = 0
        self.handlerList = ""

    def UnpackResponse(self, Response):
        super().UnpackResponse(Response)
        self.numHandlers, self.handlerList = unpack_from(
            self.ResponsePayloadFormat, Response, calcsize(self.ResponseHeaderFormat))
        return self.numHandlers, self.handlerList

    def STDOut(self):
        super().STDOut()
        self.logger.info("numHandlers: " + str(self.numHandlers))
        self.logger.info("handlerList: " + self.handlerList)


class RestartHandler(ServerGroup):
    def __init__(self, handlerName):
        super().__init__()
        self.SendCmdid = 4
        self.SendPaylen = 32
        self.handlerName = handlerName.encode()
        self.SendCmdPayloadFormat = "<32s"

    def PackCommand(self):
        super().PackCommand()
        self.SendCmdPayload = pack(self.SendCmdPayloadFormat, self.handlerName)
        self.SendCommand = self.SendCommand + self.SendCmdPayload
        return self.SendCommand
