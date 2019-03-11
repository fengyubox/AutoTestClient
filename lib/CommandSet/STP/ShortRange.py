from .Group import ShortRangeGroup, ShortRangeOnOffGroup
from struct import pack, unpack_from, calcsize


class On(ShortRangeOnOffGroup):
    def __init__(self):
        super().__init__()
        self.enable = True


class Off(ShortRangeOnOffGroup):
    def __init__(self):
        super().__init__()
        self.enable = False


class SpiCommsTest(ShortRangeGroup):
    def __init__(self):
        super().__init__()
        self.SendCmdid = 4
        self.SendPaylen = 0
        self.ResponsePayloadFormat = "<?3s"
        self.result = True
        self.padding = ""

    def UnpackResponse(self, Response):
        super().UnpackResponse(Response)
        self.result, self.padding = unpack_from(
            self.ResponsePayloadFormat, Response, calcsize(self.ResponseHeaderFormat))
        return self.result, self.padding

    def STDOut(self):
        super().STDOut()
        self.logger.info("result: " + str(self.result))


class SRFBufferTest(ShortRangeGroup):
    def __init__(self):
        super().__init__()
        self.SendCmdid = 6
        self.SendPaylen = 0
        self.ResponsePayloadFormat = "<?3s"
        self.result = True
        self.padding = ""

    def UnpackResponse(self, Response):
        super().UnpackResponse(Response)
        self.result, self.padding = unpack_from(
            self.ResponsePayloadFormat, Response, calcsize(self.ResponseHeaderFormat))
        return self.result, self.padding

    def STDOut(self):
        super().STDOut()
        self.logger.info("result: " + str(self.result))


class InterruptTest(ShortRangeGroup):
    def __init__(self):
        super().__init__()
        self.SendCmdid = 8
        self.SendPaylen = 0
        self.ResponsePayloadFormat = "<?3s"
        self.result = True
        self.padding = ""

    def UnpackResponse(self, Response):
        super().UnpackResponse(Response)
        self.result, self.padding = unpack_from(
            self.ResponsePayloadFormat, Response, calcsize(self.ResponseHeaderFormat))
        return self.result, self.padding

    def STDOut(self):
        super().STDOut()
        self.logger.info("result: " + str(self.result))


class SubGConnectTest(ShortRangeGroup):
    def __init__(self):
        super().__init__()
        self.SendCmdid = 12
        self.SendPaylen = 0
        self.ResponsePayloadFormat = "<?3s"
        self.result = False
        self.padding = ""

    def UnpackResponse(self, Response):
        super().UnpackResponse(Response)
        self.result, self.padding = unpack_from(
            self.ResponsePayloadFormat, Response, calcsize(self.ResponseHeaderFormat))
        return self.result, self.padding

    def STDOut(self):
        super().STDOut()
        self.logger.info("result: " + str(self.result))


class ResetTest(ShortRangeGroup):
    def __init__(self):
        super().__init__()
        self.SendCmdid = 16
        self.SendPaylen = 0
        self.ResponsePayloadFormat = "<?3s"
        self.result = True
        self.padding = ""

    def UnpackResponse(self, Response):
        super().UnpackResponse(Response)
        self.result, self.padding = unpack_from(
            self.ResponsePayloadFormat, Response, calcsize(self.ResponseHeaderFormat))
        return self.result, self.padding

    def STDOut(self):
        super().STDOut()
        self.logger.info("result: " + str(self.result))


class SpiIntTest(ShortRangeGroup):
    def __init__(self):
        super().__init__()
        self.SendCmdid = 18
        self.SendPaylen = 0
        self.ResponsePayloadFormat = "<?3s"
        self.result = True
        self.padding = ""

    def UnpackResponse(self, Response):
        super().UnpackResponse(Response)
        self.result, self.padding = unpack_from(
            self.ResponsePayloadFormat, Response, calcsize(self.ResponseHeaderFormat))
        return self.result, self.padding

    def STDOut(self):
        super().STDOut()
        self.logger.info("result: " + str(self.result))


class SrfWakeTest(ShortRangeGroup):
    def __init__(self):
        super().__init__()
        self.SendCmdid = 20
        self.SendPaylen = 0
        self.ResponsePayloadFormat = "<?3s"
        self.result = True
        self.padding = ""

    def UnpackResponse(self, Response):
        super().UnpackResponse(Response)
        self.result, self.padding = unpack_from(
            self.ResponsePayloadFormat, Response, calcsize(self.ResponseHeaderFormat))
        return self.result, self.padding

    def STDOut(self):
        super().STDOut()
        self.logger.info("result: " + str(self.result))


class SrfDetectTest(ShortRangeGroup):
    def __init__(self):
        super().__init__()
        self.SendCmdid = 22
        self.SendPaylen = 0
        self.ResponsePayloadFormat = "<?3s"
        self.result = True
        self.padding = ""

    def UnpackResponse(self, Response):
        super().UnpackResponse(Response)
        self.result, self.padding = unpack_from(
            self.ResponsePayloadFormat, Response, calcsize(self.ResponseHeaderFormat))
        return self.result, self.padding

    def STDOut(self):
        super().STDOut()
        self.logger.info("result: " + str(self.result))


class BootloaderPinTest(ShortRangeGroup):
    def __init__(self):
        super().__init__()
        self.SendCmdid = 24
        self.SendPaylen = 0
        self.ResponsePayloadFormat = "<?3s"
        self.result = True
        self.padding = ""

    def UnpackResponse(self, Response):
        super().UnpackResponse(Response)
        self.result, self.padding = unpack_from(
            self.ResponsePayloadFormat, Response, calcsize(self.ResponseHeaderFormat))
        return self.result, self.padding

    def STDOut(self):
        super().STDOut()
        self.logger.info("result: " + str(self.result))
