import socket
import time
import struct
import visa

# Based on mclib by Thomas Schmid (http://github.com/tschmid/mclib)

class SCPI:
    PORT = 56001

    def __init__(self, host, port=PORT):
        self.host = host
        self.port = port
        session = visa.ResourceManager()
        self.Instr = session.open_resource("TCPIP::%s::%s::SOCKET" % (self.host, str(self.port)), read_termination = '\n')
        self.Instr.timeout = 5000

    def getDevInfo(self):
        return self.Instr.query("*IDN?")
    
    def inputCmd(self):
        cmd = input('Input command > ')
        self.Instr.write(cmd, time.sleep(20))
        self.Instr.read()
    
    def test(self): 
        print(self.Instr.query(':SYSTem:LAST:ERRor?'))
        #self.Instr.write(':MMEMory:LOG:CLEar')


if __name__ == '__main__':
    dev = SCPI('192.168.1.1', 56001)
    print(dev.getDevInfo())
    try:
        print('Press Ctrl+c to exit...')
        #while True:
        #    dev.inputCmd()
        dev.test()
        print('Finish')
    except KeyboardInterrupt:
        print('interrupted!')
