from .Group import SensorsGroup
from struct import pack, unpack_from, calcsize


class ReadAccelValues(SensorsGroup):
    def __init__(self):
        super().__init__()
        self.SendCmdid = 8
        self.SendPaylen = 0
        self.ResponsePayloadFormat = "<3h2s"
        self.xAccelValue = 0
        self.yAccelValue = 1
        self.zAccelValue = 2
        self.padding = ""

    def UnpackResponse(self, Response):
        super().UnpackResponse(Response)
        self.xAccelValue,\
            self.yAccelValue,\
            self.zAccelValue,\
            self.padding = unpack_from(
                self.ResponsePayloadFormat, Response, calcsize(self.ResponseHeaderFormat))
        return self.xAccelValue, self.yAccelValue, self.zAccelValue, self.padding

    def STDOut(self):
        super().STDOut()
        self.logger.info("xAccelValue: " + str(self.xAccelValue))
        self.logger.info("yAccelValue: " + str(self.yAccelValue))
        self.logger.info("zAccelValue: " + str(self.zAccelValue))


class TestAccelGyroInterrupt(SensorsGroup):
    def __init__(self):
        super().__init__()
        self.SendCmdid = 14
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


class ReadTempValues(SensorsGroup):
    def __init__(self):
        super().__init__()
        self.SendCmdid = 12
        self.SendPaylen = 0
        self.ResponsePayloadFormat = "<iII"

    def UnpackResponse(self, Response):
        super().UnpackResponse(Response)
        self.temperatureValue,\
            self.pressureValue,\
            self.humidityValue = unpack_from(
                self.ResponsePayloadFormat, Response, calcsize(self.ResponseHeaderFormat))
        return self.temperatureValue, self.pressureValue, self.humidityValue

    def STDOut(self):
        super().STDOut()
        self.logger.info("temperatureValue: " + str(self.temperatureValue))
        self.logger.info("pressureValue: " + str(self.pressureValue))
        self.logger.info("humidityValue: " + str(self.humidityValue))


class CalibrateToFXTalk(SensorsGroup):
    def __init__(self):
        super().__init__()
        self.SendCmdid = 16
        self.SendPaylen = 4
        self.SendCmdPayloadFormat = "<B3s"
        self.numberOfSamples = 20
        self.padding = ""
        self.ResponsePayloadFormat = "<3H3B3s3H3B3s"
        #self.z1TofXtalkCalData = ""
        self.z1_iAveBaseCal = 0
        self.z1_qAveBaseCal = 0
        self.z1_gainAveBaseCal = 0
        self.z1_iAveExpCal = 0
        self.z1_qAveExpCal = 0
        self.z1_aveTempOffset = 0
        self.z1_padding = ""
        #self.z2TofXtalkCalData = ""
        self.z2_iAveBaseCal = 0
        self.z2_qAveBaseCal = 0
        self.z2_gainAveBaseCal = 0
        self.z2_iAveExpCal = 0
        self.z2_qAveExpCal = 0
        self.z2_aveTempOffset = 0
        self.z2_padding = ""

    def PackCommand(self):
        super().PackCommand()
        self.SendCmdPayload = pack(
            self.SendCmdPayloadFormat, self.numberOfSamples, self.padding.encode())
        self.SendCommand = self.SendCommand + self.SendCmdPayload
        return self.SendCommand

    def UnpackResponse(self, Response):
        super().UnpackResponse(Response)
        self.z1_iAveBaseCal,\
        self.z1_qAveBaseCal,\
        self.z1_gainAveBaseCal,\
        self.z1_iAveExpCal,\
        self.z1_qAveExpCal,\
        self.z1_aveTempOffset,\
        self.z1_padding,\
        self.z2_iAveBaseCal,\
        self.z2_qAveBaseCal,\
        self.z2_gainAveBaseCal,\
        self.z2_iAveExpCal,\
        self.z2_qAveExpCal,\
        self.z2_aveTempOffset,\
        self.z2_padding = unpack_from(self.ResponsePayloadFormat, \
                                        Response, calcsize(self.ResponseHeaderFormat))
        return self.z1_iAveBaseCal,\
                self.z1_qAveBaseCal,\
                self.z1_gainAveBaseCal,\
                self.z1_iAveExpCal,\
                self.z1_qAveExpCal,\
                self.z1_aveTempOffset,\
                self.z1_padding,\
                self.z2_iAveBaseCal,\
                self.z2_qAveBaseCal,\
                self.z2_gainAveBaseCal,\
                self.z2_iAveExpCal,\
                self.z2_qAveExpCal,\
                self.z2_aveTempOffset,\
                self.z2_padding

    def STDOut(self):
        super().STDOut()
        self.logger.info("z1_iAveBaseCal: " + str(self.z1_iAveBaseCal))
        self.logger.info("z1_qAveBaseCal: " + str(self.z1_qAveBaseCal))
        self.logger.info("z1_gainAveBaseCal: " + str(self.z1_gainAveBaseCal))
        self.logger.info("z1_iAveExpCal: " + str(self.z1_iAveExpCal))
        self.logger.info("z1_qAveExpCal: " + str(self.z1_qAveExpCal))
        self.logger.info("z1_aveTempOffset: " + str(self.z1_aveTempOffset))
        self.logger.info("z2_iAveBaseCal: " + str(self.z2_iAveBaseCal))
        self.logger.info("z2_qAveBaseCal: " + str(self.z2_qAveBaseCal))
        self.logger.info("z2_gainAveBaseCal: " + str(self.z2_gainAveBaseCal))
        self.logger.info("z2_iAveExpCal: " + str(self.z2_iAveExpCal))
        self.logger.info("z2_qAveExpCal: " + str(self.z2_qAveExpCal))
        self.logger.info("z2_aveTempOffset: " + str(self.z2_aveTempOffset))


class CalibrateToFDistanceOffset(SensorsGroup):
    def __init__(self):
        super().__init__()
        self.SendCmdid = 18
        self.SendPaylen = 8
        self.SendCmdPayloadFormat = "<B3sI"
        self.numberOfSamples = 20
        self.padding = ""
        self.distance = 40
        self.ResponsePayloadFormat = "2H"
        self.z1TofDistOffsetCal = 1
        self.z2TofDistOffsetCal = 2

    def PackCommand(self):
        super().PackCommand()
        self.SendCmdPayload = pack(
            self.SendCmdPayloadFormat, self.numberOfSamples, self.padding.encode(), self.distance)
        self.SendCommand = self.SendCommand + self.SendCmdPayload
        return self.SendCommand

    def UnpackResponse(self, Response):
        super().UnpackResponse(Response)
        self.z1TofDistOffsetCal,\
            self.z2TofDistOffsetCal = unpack_from(
                self.ResponsePayloadFormat, Response, calcsize(self.ResponseHeaderFormat))
        return self.z1TofDistOffsetCal, self.z2TofDistOffsetCal

    def STDOut(self):
        super().STDOut()
        self.logger.info("z1TofDistOffsetCal: " + str(self.z1TofDistOffsetCal))
        self.logger.info("z2TofDistOffsetCal: " + str(self.z2TofDistOffsetCal))


class CalibrateToFMagnitude(SensorsGroup):
    def __init__(self):
        super().__init__()
        self.SendCmdid = 20
        self.SendPaylen = 0
        self.ResponsePayloadFormat = "<2H2B2s"
        self.z1TofMagCal = 0
        self.z2TofMagCal = 1
        self.z1TofMagExpCal = 2
        self.z2TofMagExpCal = 3
        self.padding = ""

    def UnpackResponse(self, Response):
        super().UnpackResponse(Response)
        self.z1TofMagCal,\
            self.z2TofMagCal,\
            self.z1TofMagExpCal,\
            self.z2TofMagExpCal,\
            self.padding = unpack_from(
                self.ResponsePayloadFormat, Response, calcsize(self.ResponseHeaderFormat))
        return self.z1TofMagCal, self.z2TofMagCal, self.z1TofMagExpCal, self.z2TofMagExpCal, self.padding

    def STDOut(self):
        self.logger.info("z1TofMagCal: " + str(self.z1TofMagCal))
        self.logger.info("z2TofMagCal: " + str(self.z2TofMagCal))
        self.logger.info("z1TofMagExpCal: " + str(self.z1TofMagExpCal))
        self.logger.info("z2TofMagExpCal: " + str(self.z2TofMagExpCal))


class ResetSensorHub(SensorsGroup):
    def __init__(self):
        super().__init__()
        self.SendCmdid = 22
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


class ReadToFDistance(SensorsGroup):
    def __init__(self):
        super().__init__()
        self.SendCmdid = 24
        self.SendPaylen = 8
        self.SendCmdPayloadFormat = "<iI"
        self.zone = 1
        self.sampleCount = 20

        self.ResponsePayloadFormat = "ddf4sdd"
        self.distance = ""
        self.magnitude = ""
        self.temperature = ""
        self.padding = ""
        self.distanceMean = ""
        self.distanceMeanVariance = ""

    def PackCommand(self):
        super().PackCommand()
        self.SendCmdPayload = pack(
            self.SendCmdPayloadFormat, self.zone, self.sampleCount)
        self.SendCommand = self.SendCommand + self.SendCmdPayload
        return self.SendCommand

    def UnpackResponse(self, Response):
        super().UnpackResponse(Response)
        self.distance,\
            self.magnitude,\
            self.temperature,\
            self.padding,\
            self.distanceMean,\
            self.distanceMeanVariance = unpack_from(
                self.ResponsePayloadFormat, Response, calcsize(self.ResponseHeaderFormat))
        print(type(self.temperature))
        return self.distance, self.magnitude, self.temperature, self.padding, self.distanceMean, self.distanceMeanVariance

    def STDOut(self):
        super().STDOut()
        self.logger.info("distance: " + str(self.distance))
        self.logger.info("magnitude: " + str(self.magnitude))
        self.logger.info("temperature: " + str(self.temperature))
        self.logger.info("distanceMean: " + str(self.distanceMean))
        self.logger.info("distanceMeanVariance: " + str(self.distanceMeanVariance))


class GyroSelfTest(SensorsGroup):
    def __init__(self):
        super().__init__()
        self.SendCmdid = 2
        self.SendPaylen = 0
        self.ResponsePayloadFormat = "<I"
        self.result = ""

    def UnpackResponse(self, Response):
        super().UnpackResponse(Response)
        self.result = unpack_from(
            self.ResponsePayloadFormat, Response, calcsize(self.ResponseHeaderFormat))
        self.result = self.result[0]
        return self.result

    def STDOut(self):
        super().STDOut()
        self.logger.info("result: " + str(self.result))


class AccelSelfTest(SensorsGroup):
    def __init__(self):
        super().__init__()
        self.SendCmdid = 6
        self.SendPaylen = 0
        self.ResponsePayloadFormat = "<I"
        self.result = ""

    def UnpackResponse(self, Response):
        super().UnpackResponse(Response)
        self.result = unpack_from(
            self.ResponsePayloadFormat, Response, calcsize(self.ResponseHeaderFormat))
        self.result = self.result[0]
        return self.result

    def STDOut(self):
        super().STDOut()
        self.logger.info("result: " + str(self.result))


class ReadThermistor(SensorsGroup):
    def __init__(self):
        super().__init__()
        self.SendCmdid = 28
        self.SendPaylen = 0
        self.ResponsePayloadFormat = "<4s"
        self.result = ""

    def UnpackResponse(self, Response):
        super().UnpackResponse(Response)
        self.result = unpack_from(
            self.ResponsePayloadFormat, Response, calcsize(self.ResponseHeaderFormat))
        self.result = self.result[0]
        return self.result

    def STDOut(self):
        super().STDOut()
        self.logger.info("result: " + str(self.result))


class WakeupInterruptToggle(SensorsGroup):
    def __init__(self):
        super().__init__()
        self.SendCmdid = 30
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


class AlsIdCheck(SensorsGroup):
    def __init__(self):
        super().__init__()
        self.SendCmdid = 32
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


class TphIdCheck(SensorsGroup):
    def __init__(self):
        super().__init__()
        self.SendCmdid = 34
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
