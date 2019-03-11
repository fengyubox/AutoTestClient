''' =========================================================================================
			           Authentication - GetAuth.py
    =========================================================================================
    Class Authentication is a sepcific command extend ParentCommand. Order to generate an 
    authentication command to send before sending STP command.
    =========================================================================================

'''

from struct import pack, unpack_from, calcsize
from .ParentCommand import ParentCommand


class Authentication(ParentCommand):
    def __init__(self):
        self.auth = "0000000000000000000000000100000008000000BB10162074657374"
        #self.PackedAuth = bytes.fromhex(self.auth)

    def PackCommand(self):
        return bytes.fromhex(self.auth)

    def STDOut(self):
        self.logger.debug("SendAuth: " + self.PackCommand())
