
import visa
import time

Session = visa.ResourceManager('@py')

Instr = Session.open_resource("TCPIP::192.168.1.1::56001::SOCKET", read_termination = '\n')

Instr.write("SYST:LANG SCPI")
Instr.write("ROUT:PORT:CONN:DIR PORT1,PORT1")
Instr.write("SOUR:GPRF:GEN:MODE NORMAL")
Instr.write("SOUR:GPRF:GEN:BBM CW")
Instr.write("SOUR:GPRF:GEN:RFS:FREQ 1575.42MHz")
Instr.write("SOUR:GPRF:GEN:RFS:LEV -130.0")
Instr.write("SOUR:GPRF:GEN:STAT ON")

Instr.write("SOUR:GPRF:GEN:STAT OFF")
