
import visa
import time
import sys

Session = visa.ResourceManager('@py')

#Instr = Session.open_resource("TCPIP::192.168.1.1::56001::SOCKET", read_termination = '\n')
Instr = Session.open_resource("TCPIP::192.168.1.1::56001::SOCKET", read_termination = '\r\n', write_termination = '\r\n' )

Instr.timeout = 5000

Instr.write("SYST:LANG SCPI")
Instr.write("MMEMory:LOG:CLEar")  #clear log

# Run Spectrum Monitor
Instr.write("SYST:LANG SCPI")
Instr.write("CALC:EXTL:TABL:SETT 1")
Instr.write("SYST:LANG NAT")
Instr.write("STDSEL COMMON")
Instr.write("PORT PORT3,PORT1")
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
Instr.query("MSTAT?", 3) # need to polling until response is 0
print(Instr.query("SPMPWR?"))


