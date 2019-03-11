
import visa
import time
import sys

Session = visa.ResourceManager('@py')

Instr = Session.open_resource("TCPIP::192.168.1.1::56001::SOCKET", read_termination = '\n')

Instr.timeout=500


Instr.write("SYST:LANG SCPI")
print('System Lang is ', Instr.query("SYST:LANG?"))
print(Instr.query("*IDN?"))
Instr.write("MMEMory:LOG:CLEar")  #clear log

# =================================================
# Run commands 
#Instr.write("SYST:LANG SCPI")
Instr.write("SYST:LANG NAT")
print('System Lang is ', Instr.query("SYST:LANG?"))

#Instr.write("CALC:EXTL:TABL:SETT 1")
Instr.write("STDSEL COMMON")
Instr.write("ULFREQ 840MHZ\n")

# =================================================
Instr.write("SYST:LANG SCPI")
str = Instr.query("SYST:ERR:ALL?", time.sleep(5))
print(str)  # print error

'''
Instr.write("SYST:LANG NAT")






Instr.write("PORT PORT1,PORT3")
Instr.write("ULFREQ 840MHZ")
Instr.write("ILVL 22")
Instr.write("SPMSPAN 1MHZ")
Instr.write("SPMRBW 10KHZ")
Instr.write("SPMDETECT RMS")
Instr.write("SPMSTORAGEMODE AVG")
Instr.write("SPMSTORAGECOUNT 10")
Instr.write("SPMTIME 1MS")
Instr.write("SPMPMBW 1MHZ")
Instr.write("SPMTGSRC FREERUN")
Instr.write("SNGLS")
Instr.query("MSTAT?", time.sleep(2)) # need to polling until response is 0
print(Instr.query("SPMPWR?"))

'''

