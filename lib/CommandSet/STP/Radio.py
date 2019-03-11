from .Group import RadioGroup, RadioOnOffGroup, RadioTxOnOffGroup, RadioRxOnOffGroup
from struct import pack, unpack_from, calcsize


class ReadIMEI(RadioGroup):
    def __init__(self):
        super().__init__()
        self.SendCmdid = 2
        self.SendPaylen = 0
        self.ResponsePayloadFormat = "<20s"
        self.imei = ""

    def UnpackResponse(self, Response):
        super().UnpackResponse(Response)
        self.imei = unpack_from(
            self.ResponsePayloadFormat, Response, calcsize(self.ResponseHeaderFormat))
        self.imei = self.imei[0].decode().rstrip('\x00')
        return self.imei

    def STDOut(self):
        super().STDOut()
        self.logger.info("imei: " + repr(self.imei))


class PerformSIMCheck(RadioGroup):
    def __init__(self):
        super().__init__()
        self.SendCmdid = 8
        self.SendPaylen = 0
        self.ResponsePayloadFormat = "<28s"
        self.iccid = ""

    def UnpackResponse(self, Response):
        super().UnpackResponse(Response)
        self.iccid = unpack_from(
            self.ResponsePayloadFormat, Response, calcsize(self.ResponseHeaderFormat))
        self.iccid = self.iccid[0].decode().rstrip('\x00')
        return self.iccid

    def STDOut(self):
        super().STDOut()
        self.logger.info("iccid: " + str(self.iccid))


class EnableRadioTx(RadioTxOnOffGroup):
    def __init__(self):
        super().__init__()
        self.enable = True


class DisableRadioTx(RadioTxOnOffGroup):
    def __init__(self):
        super().__init__()
        self.enable = False


class SetupGPSPolarity(RadioGroup):
    def __init__(self):
        super().__init__()
        self.SendCmdid = 14
        self.SendPaylen = 0


class GPSCommsCheck(RadioGroup):
    def __init__(self):
        super().__init__()
        self.SendCmdid = 6
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


class RadioOn(RadioOnOffGroup):
    def __init__(self):
        super().__init__()
        self.enable = True


class RadioOff(RadioOnOffGroup):
    def __init__(self):
        super().__init__()
        self.enable = False


class ReadGPSCNo(RadioGroup):
    def __init__(self):
        super().__init__()
        self.SendCmdid = 12
        self.SendPaylen = 0
        self.ResponsePayloadFormat = "<i"
        self.gpsCNo = 3

    def UnpackResponse(self, Response):
        super().UnpackResponse(Response)
        self.gpsCNo = unpack_from(
            self.ResponsePayloadFormat, Response, calcsize(self.ResponseHeaderFormat))
        self.gpsCNo = self.gpsCNo[0]
        return self.gpsCNo

    def STDOut(self):
        super().STDOut()
        self.logger.info("gpsCNo: " + str(self.gpsCNo))


class WriteIMEI(RadioGroup):
    def __init__(self, imei):
        super().__init__()
        self.SendCmdid = 18
        self.SendPaylen = 20
        self.imei = imei
        self.SendCmdPayloadFormat = "<20s"

    def PackCommand(self):
        super().PackCommand()
        self.SendCmdPayload = pack(
            self.SendCmdPayloadFormat, self.imei.encode())
        self.SendCommand = self.SendCommand + self.SendCmdPayload
        return self.SendCommand


class SetUsbEcmMode(RadioGroup):
    def __init__(self):
        super().__init__()
        self.SendCmdid = 20
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


class ModemIDTest(RadioGroup):
    def __init__(self):
        super().__init__()
        self.SendCmdid = 22
        self.SendPaylen = 0
        self.ResponsePayloadFormat = "<B?2s"
        self.modemID = 1
        self.modemVerified = True
        self.padding = ""

    def UnpackResponse(self, Response):
        super().UnpackResponse(Response)
        self.modemID,\
            self.modemVerified,\
            self.padding = unpack_from(
                self.ResponsePayloadFormat, Response, calcsize(self.ResponseHeaderFormat))
        return self.modemID, self.modemVerified, self.padding

    def STDOut(self):
        super().STDOut()
        self.logger.info("modemID: " + str(self.modemID))
        self.logger.info("modemVerified: " + str(self.modemVerified))


class ModemBufferTest(RadioGroup):
    def __init__(self):
        super().__init__()
        self.SendCmdid = 24
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


class GPSBufferTest(RadioGroup):
    def __init__(self):
        super().__init__()
        self.SendCmdid = 28
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


class EnableRadioRx(RadioRxOnOffGroup):
    def __init__(self, secondaryAnt):
        super().__init__()
        self.enable = True
        self.secondaryAnt = secondaryAnt


class DisableRadioRx(RadioRxOnOffGroup):
    def __init__(self, secondaryAnt):
        super().__init__()
        self.enable = False
        self.secondaryAnt = secondaryAnt
