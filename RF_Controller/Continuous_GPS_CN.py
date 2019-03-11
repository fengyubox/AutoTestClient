
import visa
import time

Session = visa.ResourceManager('@py')

Instr = Session.open_resource("TCPIP::192.168.1.1::56001::SOCKET", read_termination = '\n')

Instr.write("SYST:LANG SCPI")
Instr.write("CALC:EXTL:TABL:SETT 1")
Instr.write("ROUT:PORT:CONN:DIR PORT1,PORT1")
Instr.write("SOUR:GPRF:GEN:MODE NORMAL")
Instr.query("SOUR:GPRF:GEN:ARB:FILE:LOAD? 'MV887100A_GPS_0002'") # need to check if the waveform is loaded or not
Instr.write("SOUR:GPRF:GEN:ARB:FILE:LOAD 'MV887100A_GPS_0002'")
while True:
	res = Instr.query("SOUR:GPRF:GEN:ARB:FILE:LOAD:STAT?") # need to polling until the response is 0
	print('Load waveform result:', res)
	if int(res) == 0:
		break	
Instr.write("SOUR:GPRF:GEN:RFS:FREQ 1575.42MHZ")
Instr.write("SOUR:GPRF:GEN:RFS:LEV -100")
Instr.write("SOUR:GPRF:GEN:BBM ARB")
Instr.write("SOUR:GPRF:GEN:ARB:NOIS:STAT OFF")
Instr.write("SOUR:GPRF:GEN:RFS:DM:POL NORMAL")
Instr.write("SOUR:GPRF:GEN:ARB:WAV:SSW FIXED,0")
Instr.write("SOUR:GPRF:GEN:ARB:WAV:SYNC:STAR:CANC")
Instr.write("SOUR:GPRF:GEN:ARB:WAV:PATT:SEL 'MV887100A_GPS_0002', 1, 1")
Instr.write("SOUR:GPRF:GEN:STAT ON")


# Instr.write("SOUR:GPRF:GEN:STAT OFF")
