from .RF_Client import RF_Client
import time
from Config.RamaConfig import MT8870A_Config
from Utility.Logger.RamaLogger import RamaLogger


class Anritsu_MT8870A(RF_Client):

    def __init__(self, host='192.168.1.1', port=56001, timeout=2):
        super().__init__(host, port, timeout)
        self.logger = RamaLogger().getLogger()
        self.InitDevice()

    def InitDevice(self):
        self.instr.write("*CLS")
        self.instr.query("*ESR?")
        self.instr.write("SYST:LANG SCPI")
        self.instr.query("*OPC?")
        self.instr.query("*ESR?")
        self.instr.query("SYST:ERR:COUN?")
        self.instr.query("*ESR?")
        self.instr.query("SYST:ERR:ALL?")
        self.instr.query("*ESR?")
        self.instr.write("INST:SEL SRW")
        self.instr.query("*OPC?")
        self.instr.query("*ESR?")
        self.instr.query("SYST:VERS?")
        self.instr.query("SYST:INF:MAIN:DEV:ID?")
        # self.instr.write("CALC:CAL:BAND:STAR:TEMP 2")
        self.instr.query("*OPC?")
        self.instr.query("*ESR?")
        self.instr.query("*OPC?")
        self.instr.query("*IDN?")
        self.instr.write("CALC:EXTL:TABL:SETT 1")
        self.instr.write("CALC:EXTL:TABL:DEL")
        self.instr.write("CALC:EXTL:TABL:VAL:ALL 880.03MHZ, 20, 20, 20, 20, 20, \
                         20, 20, 20")
        self.instr.write("EXTL:TABL:SWIT ON")

    def DisableStat(self):
        self.instr.write("SOUR:GPRF:GEN:STAT OFF")

    def SendGPS(self):
        self.instr.write("SYST:LANG SCPI")
        self.instr.write("CALC:EXTL:TABL:SETT 1")
        self.instr.write("ROUT:PORT:CONN:DIR PORT1,PORT")
        self.instr.write("SOUR:GPRF:GEN:MODE NORMAL")
        self.instr.write("SOUR:GPRF:GEN:STAT ON")
        self.instr.write("SOUR:GPRF:GEN:BBM CW")
        # Set RF output frequency
        self.instr.write("SOUR:GPRF:GEN:RFS:FREQ 1575.42MHZ")
        # Set RF output level
        self.instr.write("SOUR:GPRF:GEN:RFS:LEV -120")
        self.instr.query("SOUR:GPRF:GEN:ARB:FILE:LOAD? 'MV887100A_GPS_0002'")
        self.instr.write("SOUR:GPRF:GEN:ARB:FILE:LOAD 'MV887100A_GPS_0002'")
        while True:
            # need to polling until the response is 0
            res = self.instr.query("SOUR:GPRF:GEN:ARB:FILE:LOAD:STAT?")
            if int(res) == 0:
                break
        self.instr.write("SOUR:GPRF:GEN:ARB:WAV:PATT:SEL 'MV887100A_GPS_0002', 1")
        self.instr.write("SOUR:GPRF:GEN:BBM ARB")
        self.logger.info('Send GPS signal.')

    def ReadRadioTx(self):
        self.instr.write("SYST:LANG NAT")
        self.instr.write("LOSSTBL 1")
        self.instr.write("SYSSEL Cellular")
        self.instr.write("STDSEL COMMON")
        self.instr.write("PORT PORT1,PORT3")
        self.instr.write("ULFREQ 840MHZ")
        self.instr.write("ILVL 22")
        self.instr.write("SPMSPAN 1MHZ")
        self.instr.write("SPMRBW 10KHZ")
        self.instr.write("SPMDETECT RMS")
        self.instr.write("SPMSTORAGEMODE AVG")
        self.instr.write("SPMSTORAGECOUNT 10")
        self.instr.write("SPMTIME 1MS")
        self.instr.write("SPMPMBW 1MHZ")
        self.instr.write("SPMTGSRC FREERUN")
        # Start auto level measurement and query status
        self.instr.write("SNGLS")
        while True:
            # need to polling until response is 0
            res = self.instr.query("MSTAT?", time.sleep(10))
            if int(res) == 0:
                break
        # Query measurement results
        return float(self.instr.query("SPMPWR?"))

    def EnableRadioRx(self):
        self.instr.write("SYST:LANG SCPI")
        self.instr.write("ROUT:PORT:CONN:DIR PORT%d,PORT%d" %
                         (MT8870A_Config.getint('RX_Measurement',
                                                'Input_Port'),
                          MT8870A_Config.getint('RX_Measurement',
                                                'Output_Port')))
        self.instr.write("SOUR:GPRF:GEN:MODE NORMAL")
        self.instr.write("SOUR:GPRF:GEN:BBM CW")
        self.instr.write("SOUR:GPRF:GEN:RFS:FREQ %s" %
                         MT8870A_Config.get('RX_Measurement', 'Frequency'))
        self.instr.write("SOUR:GPRF:GEN:RFS:LEV %d" %
                         MT8870A_Config.getint('RX_Measurement', 'Level'))
        self.instr.write("SOUR:GPRF:GEN:STAT ON")
