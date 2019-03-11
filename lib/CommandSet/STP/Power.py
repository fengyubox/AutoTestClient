from .Group import PowerGroup
from struct import pack, unpack_from, calcsize


class GetBatteryVoltage(PowerGroup):
    def __init__(self):
        super().__init__()
        self.SendCmdid = 2
        self.SendPaylen = 0
        self.ResponsePayloadFormat = "<I"
        self.voltageValue = ""

    def UnpackResponse(self, Response):
        super().UnpackResponse(Response)
        self.voltageValue = unpack_from(
            self.ResponsePayloadFormat, Response, calcsize(self.ResponseHeaderFormat))
        self.voltageValue = self.voltageValue[0]
        return self.voltageValue

    def STDOut(self):
        super().STDOut()
        self.logger.info("voltageValue: " + str(self.voltageValue))


class SetPowerLevel (PowerGroup):
    def __init__(self, powerLevel):
        super().__init__()
        self.SendCmdid = 4
        self.SendPaylen = 4
        self.powerLevel = powerLevel
        self.SendCmdPayloadFormat = "<i"

    def PackCommand(self):
        super().PackCommand()
        self.SendCmdPayload = pack(self.SendCmdPayloadFormat, self.powerLevel)
        self.SendCommand = self.SendCommand + self.SendCmdPayload
        return self.SendCommand


class GetBatteryIDLineVoltage(PowerGroup):
    def __init__(self):
        super().__init__()
        self.SendCmdid = 6
        self.SendPaylen = 0
        self.ResponsePayloadFormat = "<I"
        self.voltageValue = None

    def UnpackResponse(self, Response):
        super().UnpackResponse(Response)
        self.voltageValue = unpack_from(
            self.ResponsePayloadFormat, Response, calcsize(self.ResponseHeaderFormat))
        self.voltageValue = self.voltageValue[0]
        return self.voltageValue

    def STDOut(self):
        super().STDOut()
        self.logger.info("voltageValue: " + str(self.voltageValue))

class FuelGaugeTest(PowerGroup):
    def __init__(self):
        super().__init__()
        self.SendCmdid = 8
        self.SendPaylen = 0
        self.ResponsePayloadFormat = "<HhhH?3s"
        self.voltageValue = None
        self.tempValue = None
        self.currentValue = None
        self.deviceID = None
        self.interruptStatus = None
        self.padding = ""

    def UnpackResponse(self, Response):
        super().UnpackResponse(Response)
        self.voltageValue,\
        self.tempValue,\
        self.currentValue,\
        self.deviceID,\
        self.interruptStatus,\
        self.padding = unpack_from(
            self.ResponsePayloadFormat, Response, calcsize(self.ResponseHeaderFormat))

        return self.voltageValue, self.tempValue, self.currentValue, self.deviceID, self.interruptStatus

    def STDOut(self):
        super().STDOut()
        self.logger.info("voltageValue: " + str(self.voltageValue))
        self.logger.info("tempValue: " + str(self.tempValue))
        self.logger.info("currentValue: " + str(self.currentValue))
        self.logger.info("deviceID: " + str(self.deviceID))
        self.logger.info("interruptStatus: " + str(self.interruptStatus))
        
