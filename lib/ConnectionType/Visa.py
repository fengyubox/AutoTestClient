import socket
import visa
import time
import logging
from .IConnectionType import ConnectionType


class VisaConnection(ConnectionType):
    def __init__(self, host, port, recvTimeout=20):
        self.logger = logging.getLogger('RamaLogger')
        self.host = host
        self.port = port
        self.session = visa.ResourceManager('@py')
        self.Connect()

    def Connect(self):
        '''Connect to target device.''' 
        self.instr = self.session.open_resource("TCPIP::%s::%s::SOCKET" % (self.host, str(self.port)), read_termination = '\n')
        self.instr.timeout = 2000
        self.logger.info("Already connect to %s:%s" % (self.host,self.port))

    def Send(self, cmd):
        self.instr.write(cmd)

    def Receive(self, response_length):
        self.instr.read()

    def Disconnect(self):
        '''Disconnect to target device.'''
        self.instr.close()

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
        self.instr.write("CALC:CAL:BAND:STAR:TEMP 2")
        self.instr.query("*OPC?")
        self.instr.query("*ESR?")
        self.instr.query("*OPC?")
        self.instr.query("*IDN?")
        self.instr.write("CALC:EXTL:TABL:SETT 1")
        self.instr.write("CALC:EXTL:TABL:DEL")
        self.instr.write("CALC:EXTL:TABL:VAL:ALL 840MHZ,20,20,20,20,20,20,20,20")
        self.instr.write("EXTL:TABL:SWIT ON")
    
    def SendGPS(self):
        self.instr.write("SYST:LANG SCPI")
        self.instr.write("CALC:EXTL:TABL:SETT 1")
        self.instr.write("ROUT:PORT:CONN:DIR PORT1,PORT1")
        self.instr.write("SOUR:GPRF:GEN:MODE NORMAL")
        self.instr.query("SOUR:GPRF:GEN:ARB:FILE:LOAD? 'MV887100A_GPS_0002'") # need to check if the waveform is loaded or not
        self.instr.write("SOUR:GPRF:GEN:ARB:FILE:LOAD 'MV887100A_GPS_0002'")
        while True:
            res = self.instr.query("SOUR:GPRF:GEN:ARB:FILE:LOAD:STAT?") # need to polling until the response is 0
            if int(res) == 0:
                break	
        self.instr.write("SOUR:GPRF:GEN:RFS:FREQ 1575.42MHZ") # Set RF output frequency
        self.instr.write("SOUR:GPRF:GEN:RFS:LEV -120")  # Set RF output level
        self.instr.write("SOUR:GPRF:GEN:BBM ARB")
        self.instr.write("SOUR:GPRF:GEN:ARB:NOIS:STAT OFF")
        self.instr.write("SOUR:GPRF:GEN:RFS:DM:POL NORMAL")
        self.instr.write("SOUR:GPRF:GEN:ARB:WAV:SSW FIXED,0")
        self.instr.write("SOUR:GPRF:GEN:ARB:WAV:SYNC:STAR:CANC")
        self.instr.write("SOUR:GPRF:GEN:ARB:WAV:PATT:SEL 'MV887100A_GPS_0002', 1, 1")
        self.instr.write("SOUR:GPRF:GEN:STAT ON")
        print('Send GPS signal.')
    
    def DisableGPS(self):
        self.instr.write("SOUR:GPRF:GEN:STAT OFF")

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
            res = self.instr.query("MSTAT?", time.sleep(10)) # need to polling until response is 0
            if int(res) == 0:
                break
        # Query measurement results
        return float(self.instr.query("SPMPWR?")) 

    def EnableRadioRx(self):
        self.instr.write("SYST:LANG SCPI")
        self.instr.write("ROUT:PORT:CONN:DIR PORT1,PORT1")
        self.instr.write("SOUR:GPRF:GEN:MODE NORMAL")
        self.instr.write("SOUR:GPRF:GEN:BBM CW")
        self.instr.write("SOUR:GPRF:GEN:RFS:FREQ 1575.42MHz")
        self.instr.write("SOUR:GPRF:GEN:RFS:LEV -130.0")
        self.instr.write("SOUR:GPRF:GEN:STAT ON")
    
    def DisableRadioRx(self):
        self.instr.write("SOUR:GPRF:GEN:STAT OFF")