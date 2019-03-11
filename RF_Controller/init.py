
import visa

Session = visa.ResourceManager('@py')

Instr = Session.open_resource("TCPIP::192.168.1.1::56001::SOCKET", read_termination = '\n')
Instr.timeout=200

Instr.write("*CLS")
print(Instr.query("*ESR?"))
Instr.write("SYST:LANG SCPI")
print(Instr.query("*OPC?"))
print(Instr.query("*ESR?"))
print(Instr.query("SYST:ERR:COUN?"))
print(Instr.query("*ESR?"))
print(Instr.query("SYST:ERR:ALL?"))
print(Instr.query("*ESR?"))
Instr.write("INST:SEL SRW")
print(Instr.query("*OPC?"))
print(Instr.query("*ESR?"))
print(Instr.query("SYST:VERS?"))
print(Instr.query("SYST:INF:MAIN:DEV:ID?"))
Instr.write("CALC:CAL:BAND:STAR:TEMP 2")
print(Instr.query("*OPC?"))
print(Instr.query("*ESR?"))
print(Instr.query("*OPC?"))
print(Instr.query("*IDN?"))

Instr.write("CALC:EXTL:TABL:SETT 1")
Instr.write("CALC:EXTL:TABL:DEL")
Instr.write("CALC:EXTL:TABL:VAL:ALL 840MHZ,20,20,20,20,20,20,20,20")
Instr.write("EXTL:TABL:SWIT ON")
