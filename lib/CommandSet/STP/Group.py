'''
===============================================================================
 Child STP Command - Group.py
===============================================================================
Some child classes extend attribute and function of ParentCommand. Define
SendGroupid depend on different group individually.
===============================================================================

'''
from .ParentCommand import ParentCommand
from struct import pack, unpack_from, calcsize


class ServerGroup(ParentCommand):
    def __init__(self):
        super().__init__()
        self.SendGroupid = 0


class SystemGroup(ParentCommand):
    def __init__(self):
        super().__init__()
        self.SendGroupid = 1


class PowerGroup(ParentCommand):
    def __init__(self):
        super().__init__()
        self.SendGroupid = 2


class RadioGroup(ParentCommand):
    def __init__(self):
        super().__init__()
        self.SendGroupid = 3


class RadioOnOffGroup(RadioGroup):
    def __init__(self):
        super().__init__()
        self.SendCmdid = 16
        self.SendPaylen = 4
        self.padding = ""
        self.SendCmdPayloadFormat = "<?3s"
        self.ResponsePayloadFormat = "<I"
        self.result = ""
        self.enable = None

    def PackCommand(self):
        super().PackCommand()
        self.SendCmdPayload = pack(
            self.SendCmdPayloadFormat, self.enable, self.padding.encode())
        self.SendCommand = self.SendCommand + self.SendCmdPayload
        return self.SendCommand

    def UnpackResponse(self, Response):
        super().UnpackResponse(Response)
        self.result = unpack_from(
            self.ResponsePayloadFormat, Response, calcsize(self.ResponseHeaderFormat))
        self.result = self.result[0]
        return self.result

    def STDOut(self):
        super().STDOut()
        self.logger.info("result: " + repr(self.result))


class RadioTxOnOffGroup(RadioGroup):
    def __init__(self):
        super().__init__()
        self.SendCmdid = 10
        self.SendPaylen = 16
        self.enable = None
        self.padding = ""
        self.radioBand = 7
        self.radioChannel = 4200
        self.powerLevel = 8
        self.SendCmdPayloadFormat = "<?3s3i"

        self.ResponsePayloadFormat = "<?3s"
        self.result = ""

    def PackCommand(self):
        super().PackCommand()
        self.SendCmdPayload = pack(self.SendCmdPayloadFormat,
                                   self.enable, self.padding.encode(),
                                   self.radioBand, self.radioChannel,
                                   self.powerLevel)
        self.SendCommand = self.SendCommand + self.SendCmdPayload
        return self.SendCommand

    def UnpackResponse(self, Response):
        super().UnpackResponse(Response)
        self.result,\
            self.padding = unpack_from(
                self.ResponsePayloadFormat, Response, calcsize(self.ResponseHeaderFormat))
        self.padding = self.padding.decode()
        return self.result

    def STDOut(self):
        super().STDOut()
        self.logger.info("result: " + repr(self.result))


class RadioRxOnOffGroup(RadioGroup):
    def __init__(self):
        super().__init__()
        self.SendCmdid = 30
        self.SendPaylen = 16
        self.enable = None
        self.secondaryAnt = True
        self.padding = ""
        self.radioBand = 7
        self.radioChannel = 4400
        self.durationInMs = 10000
        self.SendCmdPayloadFormat = "<??2s3i"

        self.ResponsePayloadFormat = "<3b1s"
        self.result = ""

    def PackCommand(self):
        super().PackCommand()
        self.SendCmdPayload = pack(self.SendCmdPayloadFormat,
                                   self.enable, self.secondaryAnt,
                                   self.padding.encode(),
                                   self.radioBand, self.radioChannel,
                                   self.durationInMs)
        self.SendCommand = self.SendCommand + self.SendCmdPayload
        return self.SendCommand

    def UnpackResponse(self, Response):
        super().UnpackResponse(Response)
        self.rxMin,\
        self.rxAvg,\
        self.rxMax,\
        self.padding = unpack_from(
                self.ResponsePayloadFormat, Response, calcsize(self.ResponseHeaderFormat))
        self.padding = self.padding.decode()
        return self.rxMin,self.rxAvg,self.rxMax

    def STDOut(self):
        super().STDOut()
        self.logger.info("rxMin: " + str(self.rxMin))
        self.logger.info("rxAvg: " + str(self.rxAvg))
        self.logger.info("rxMax: " + str(self.rxMax))


class SensorsGroup(ParentCommand):
    def __init__(self):
        super().__init__()
        self.SendGroupid = 4


class ShortRangeGroup(ParentCommand):
    def __init__(self):
        super().__init__()
        self.SendGroupid = 5


class ShortRangeOnOffGroup(ShortRangeGroup):
    def __init__(self):
        super().__init__()
        self.SendCmdid = 2
        self.SendPaylen = 4
        self.padding = ""
        self.SendCmdPayloadFormat = "<?3s"
        # Unknown ResponsePayloadFormat ?
        self.ResponsePayloadFormat = "<I"
        # Unknown type of result
        self.result = ""
        self.enable = False

    def PackCommand(self):
        super().PackCommand()
        self.SendCmdPayload = pack(
            self.SendCmdPayloadFormat, self.enable, self.padding.encode())
        self.SendCommand = self.SendCommand + self.SendCmdPayload
        return self.SendCommand

    def STDOut(self):
        super().STDOut()
        self.logger.info("result: " + str(self.result))


class GetSetBSNGroup(SystemGroup):
    def __init__(self):
        super().__init__()
        self.SendCmdid = 14
        self.SendPaylen = 68
        self.getOrSetCommand = None
        self.bsnToSet = ""
        self.SendCmdPayloadFormat = "<I64s"
        self.ResponsePayloadFormat = "<64s"
        self.bsn = None

    def PackCommand(self):
        super().PackCommand()
        self.SendCmdPayload = pack(self.SendCmdPayloadFormat,
                                   self.getOrSetCommand,
                                   self.bsnToSet.encode())
        self.SendCommand = self.SendCommand + self.SendCmdPayload
        return self.SendCommand

    def UnpackResponse(self, Response):
        super().UnpackResponse(Response)
        self.bsn = unpack_from(self.ResponsePayloadFormat,
                               Response, calcsize(self.ResponseHeaderFormat))
        self.bsn = self.bsn[0].decode().rstrip('\x00')
        return self.bsn

    def STDOut(self):
        super().STDOut()
        self.logger.info("bsn: " + self.bsn)


class GetSetSensorBSNGroup(SystemGroup):
    def __init__(self):
        super().__init__()
        self.SendCmdid = 18
        self.SendPaylen = 16
        self.getOrSetCommand = None
        self.sensorBsnToSet = ""
        self.SendCmdPayloadFormat = "<I12s"
        self.ResponsePayloadFormat = "<12s"
        self.sensorBsn = ""

    def PackCommand(self):
        super().PackCommand()
        self.SendCmdPayload = pack(self.SendCmdPayloadFormat,
                                   self.getOrSetCommand,
                                   self.sensorBsnToSet.encode())
        self.SendCommand = self.SendCommand + self.SendCmdPayload
        return self.SendCommand

    def UnpackResponse(self, Response):
        super().UnpackResponse(Response)
        self.sensorBsn = unpack_from(self.ResponsePayloadFormat,
                                     Response, calcsize(self.ResponseHeaderFormat))
        self.sensorBsn = self.sensorBsn[0].decode().rstrip('\x00')
        return self.sensorBsn

    def STDOut(self):
        super().STDOut()
        self.logger.info("sensorBsn: " + self.sensorBsn)


class GetSetRepairBSNGroup(SystemGroup):
    def __init__(self):
        super().__init__()
        self.SendCmdid = 22
        self.SendPaylen = 68
        self.getOrSetCommand = None
        self.bsnToSet = ""
        self.SendCmdPayloadFormat = "<I64s"
        self.ResponsePayloadFormat = "<64s"
        self.bsn = None

    def PackCommand(self):
        super().PackCommand()
        self.SendCmdPayload = pack(self.SendCmdPayloadFormat,
                                   self.getOrSetCommand,
                                   self.bsnToSet.encode())
        self.SendCommand = self.SendCommand + self.SendCmdPayload
        return self.SendCommand

    def UnpackResponse(self, Response):
        super().UnpackResponse(Response)
        self.bsn = unpack_from(self.ResponsePayloadFormat,
                               Response, calcsize(self.ResponseHeaderFormat))
        self.bsn = self.bsn[0].decode().rstrip('\x00')
        return self.bsn

    def STDOut(self):
        super().STDOut()
        self.logger.info("bsn: " + self.bsn)

