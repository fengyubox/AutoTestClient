from struct import pack, unpack_from, calcsize
from .Group import SystemGroup, GetSetBSNGroup, GetSetSensorBSNGroup, GetSetRepairBSNGroup


class GetSwVersion(SystemGroup):
    def __init__(self):
        super().__init__()
        self.SendCmdid = 2
        self.SendPaylen = 0
        self.ResponsePayloadFormat = "<32s"
        self.swVersion = ""

    def UnpackResponse(self, Response):
        super().UnpackResponse(Response)
        self.swVersion = unpack_from(
            self.ResponsePayloadFormat, Response, calcsize(self.ResponseHeaderFormat))
        self.swVersion = self.swVersion[0].decode().rstrip('\x00')
        return self.swVersion

    def STDOut(self):
        super().STDOut()
        self.logger.info("swVersion: " + self.swVersion)


class WriteDeviceCerts(SystemGroup):
    def __init__(self, privateKey, privateKeyLength, certificate, certLength, csrFile, csrLength):
        super().__init__()
        self.SendCmdid = 4
        self.SendPaylen = 5132
        self.privateKey = ""
        self.privateKeyLength = 1
        self.certificate = ""
        self.certLength = 2
        self.csrFile = ""
        self.csrLength = 3
        self.SendCmdPayloadFormat = "<1024sI3072sI1024sI"

    def PackCommand(self):
        super().PackCommand()
        self.SendCmdPayload = pack(self.SendCmdPayloadFormat,
                                   self.privateKey.encode(),
                                   self.privateKeyLength,
                                   self.certificate.encode(),
                                   self.certLength,
                                   self.csrFile.encode(),
                                   self.csrLength)
        self.SendCommand = self.SendCommand + self.SendCmdPayload
        return self.SendCommand


class MemorySelfTest(SystemGroup):
    def __init__(self):
        super().__init__()
        self.SendCmdid = 6
        self.SendPaylen = 0
        self.ResponsePayloadFormat = "<?3sI"
        self.result = True
        self.padding = ""
        self.failedLines = 5

    def UnpackResponse(self, Response):
        super().UnpackResponse(Response)
        self.result,\
            self.padding,\
            self.failedLines = unpack_from(
                self.ResponsePayloadFormat, Response, calcsize(self.ResponseHeaderFormat))
        return self.result, self.padding, self.failedLines

    def STDOut(self):
        super().STDOut()
        self.logger.info("result: " + str(self.result))
        self.logger.info("failedLines: " + str(self.failedLines))


class TestI2C(SystemGroup):
    def __init__(self):
        super().__init__()
        self.SendCmdid = 8
        self.SendPaylen = 0
        self.ResponsePayloadFormat = "<?3s"
        self.result = True
        self.padding = ""

    def UnpackResponse(self, Response):
        super().UnpackResponse(Response)
        self.result,\
            self.padding = unpack_from(
                self.ResponsePayloadFormat, Response, calcsize(self.ResponseHeaderFormat))
        return self.result, self.padding

    def STDOut(self):
        super().STDOut()
        self.logger.info("result: " + str(self.result))


class EMMCSelfTest(SystemGroup):
    def __init__(self):
        super().__init__()
        self.SendCmdid = 10
        self.SendPaylen = 0
        self.ResponsePayloadFormat = "<?3s"
        self.result = True
        self.padding = ""

    def UnpackResponse(self, Response):
        super().UnpackResponse(Response)
        self.result,\
            self.padding = unpack_from(
                self.ResponsePayloadFormat, Response, calcsize(self.ResponseHeaderFormat))
        return self.result, self.padding

    def STDOut(self):
        super().STDOut()
        self.logger.info("result: " + str(self.result))


class SensorBoardEEPROMSelfTest(SystemGroup):
    def __init__(self):
        super().__init__()
        self.SendCmdid = 12
        self.SendPaylen = 0
        self.ResponsePayloadFormat = "<?3s"
        self.result = True
        self.padding = ""

    def UnpackResponse(self, Response):
        super().UnpackResponse(Response)
        self.result,\
            self.padding = unpack_from(
                self.ResponsePayloadFormat, Response, calcsize(self.ResponseHeaderFormat))
        return self.result, self.padding

    def STDOut(self):
        super().STDOut()
        self.logger.info("result: " + str(self.result))


class GetBSN(GetSetBSNGroup):
    def __init__(self):
        super().__init__()
        self.getOrSetCommand = 0


class SetBSN(GetSetBSNGroup):
    def __init__(self, bsnToSet):
        super().__init__()
        self.getOrSetCommand = 1
        self.bsnToSet = bsnToSet


class ClearDeviceCerts(SystemGroup):
    def __init__(self):
        super().__init__()
        self.SendCmdid = 16
        self.SendPaylen = 0
        self.ResponsePayloadFormat = "<?3s"
        self.removed = True
        self.padding = ""

    def UnpackResponse(self, Response):
        super().UnpackResponse(Response)
        self.removed,\
            self.padding = unpack_from(
                self.ResponsePayloadFormat, Response, calcsize(self.ResponseHeaderFormat))
        return self.removed, self.padding

    def STDOut(self):
        super().STDOut()
        self.logger.info("removed: " + str(self.removed))


class GetSensorBSN(GetSetSensorBSNGroup):
    def __init__(self):
        super().__init__()
        self.getOrSetCommand = 0


class SetSensorBSN(GetSetSensorBSNGroup):
    def __init__(self, sensorBsnToSet):
        super().__init__()
        self.getOrSetCommand = 1
        self.sensorBsnToSet = sensorBsnToSet


class CheckCertsPresent(SystemGroup):
    def __init__(self):
        super().__init__()
        self.SendCmdid = 20
        self.SendPaylen = 0
        self.ResponsePayloadFormat = "<?3s"
        self.present = True
        self.padding = ""

    def UnpackResponse(self, Response):
        super().UnpackResponse(Response)
        self.present,\
            self.padding = unpack_from(
                self.ResponsePayloadFormat, Response, calcsize(self.ResponseHeaderFormat))
        return self.present, self.padding

    def STDOut(self):
        super().STDOut()
        self.logger.info("present: " + str(self.present))


class GetRepairBSN(GetSetRepairBSNGroup):
    def __init__(self):
        super().__init__()
        self.getOrSetCommand = 0


class SetRepairBSN(GetSetRepairBSNGroup):
    def __init__(self, bsnToSet):
        super().__init__()
        self.getOrSetCommand = 1
        self.bsnToSet = bsnToSet
