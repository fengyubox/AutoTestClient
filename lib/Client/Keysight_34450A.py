import visa
from .DC_Client import DC_Client
from Utility.Logger.RamaLogger import RamaLogger


class Keysight_34450A(DC_Client):

    def __init__(self, resource="USB0::10893::45848::MY58090059::0::INSTR",
                 timeout=2):
        rm = visa.ResourceManager('@py')
        instr_list = rm.list_resources()
        resource = instr_list[0]
        super().__init__(resource, timeout)
        self.logger = RamaLogger().getLogger()
        self.logger.info("Keysight_34450A resoure = %s" % resource)

    def MeasureCurrent(self):
        return(self.instr.query("READ?"))
