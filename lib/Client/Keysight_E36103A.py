from .DC_Client import DC_Client
from Utility.Logger.RamaLogger import RamaLogger


class Keysight_E36103A(DC_Client):

    def __init__(self, resource="TCPIP0::192.168.10.2::inst0::INSTR",
                 timeout=2):
        super().__init__(resource, timeout)
        self.logger = RamaLogger().getLogger()

    def SetVoltOutput(self, volt="3.6"):
        self.logger.info("Set power to DC %s" % volt)
        self.instr.write("SOUR:VOLT %s" % volt)
        self.instr.write("OUTP:STAT ON")

    def DisableStat(self):
        self.instr.write("OUTP:STAT OFF")

    def MeasureCurrent(self):
        return(self.instr.query("MEAS:CURR:DC?"))
