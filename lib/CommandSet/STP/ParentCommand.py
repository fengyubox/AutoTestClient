''' =========================================================================================
								 Parent STP Command - ParentCommand.py
    =========================================================================================
    A parent class to define common attribute and two function which is to pack header of 
	command and unpack header of response. Order to communicate with STPServer, Test PC 
	should send the suitable format command to STPServer by TCP/IP socket.
	
	Command Format
	Field       Type(Size)      Description
	unused      (32bits) 		Internal use only, set to zeroes
	cmdid		uint32_t        command ID
	grpid       unit32_t        group ID
	version     unit32_t        The version of the request/response, starting at '1'.
	paylen      unit32_t        The length of the following payload, in bytes.
	payload     (Depend on CMD) (Depend on CMD)              

	STP Command "GetSwVersion" with no payload for example:
	    unused    cmdid     grpid     version   paylen 
    Ex: 00000000  00000002  00000001  00000001  00000000
	=========================================================================================
	Before Test PC communicate with STPServer, the sending command should be packed in
	advance. About sending command, there are two parts. Before send the real STP Command
	which is above "GetSwVersion", Test PC should send an authentication packet. After that,
	send the real STP Command which is also packed in advance.
	The step is similar with receiving corresponding message from STPServer. After receiving 
	message through socket program, Test PC should unpack the message.	

	This STPCommand class is defined for all of STP Command and Response to be packed and 
	unpack before and after communicating with STPServer.
	There are three function to combine entire data pack and unpack.
	GetAuth()  : Get authentication packet.
	GetCMD()   : Get packed STP Command.
	DecodeMsg(): Unpack the message from STPServer to Response Format.
	=========================================================================================
	Response Payload
    Field           Type(Size)         Description
	unused      	(32bits) 	       Internal use only, set to zeroes
	cmdid			uint32_t       	   command ID will be incremented by one.
	grpid       	unit32_t           group ID
	version     	unit32_t    	   The version of the request/response, starting at '1'.
	paylen      	unit32_t  	       The length of the following ResultCode+ResultMessage, 
									   in bytes.
    ResultCode      uint32_t           The status code of the command.
    ResultMessage   char(1024 bytes)   Result message that can be optionally set by the command.
	=========================================================================================
'''
import logging
import socket
from struct import pack, unpack_from, calcsize
from Config.RamaConfig import Config
from Utility.Logger.RamaLogger import RamaLogger

class ParentCommand:
    def __init__(self):
        self.logger = RamaLogger().getLogger()
        # SendCommand----------------------------------------------------------
        # Command Header
        # Unused (32 bits) Internal use only, set to zeroes
        self.SendUnused = 0
        # The Version is 1
        self.SendVersion = 1
        # Default
        self.SendGroupid = 2
        self.SendCmdid = 3
        self.SendPaylen = 4
        # Command pack format, depend on Command Payload
        self.SendCmdHeaderFormat = "<5I"
        self.SendCmdPayloadFormat = ""
        self.SendCommand = ""
        # ReceiveResponse----------------------------------------------------------
        # Response unpack format, depend on command-specific response payload
        self.ResponsePayloadFormat = ""
        self.ResponseHeaderFormat = "<5II1024s"
        # Default
        self.RecvUnused = 0
        self.RecvGroupid = 0
        self.RecvCmdid = 0
        self.RecvVersion = 0
        self.RecvPaylen = 0
        self.ResultCode = 0
        self.ResultMsg = ""
        #######################################################

    def PackCommand(self):
        # Pack Command Header to SendCommand.
        self.SendCommand = pack(self.SendCmdHeaderFormat,
                                self.SendUnused, self.SendCmdid,
                                self.SendGroupid, self.SendVersion,
                                self.SendPaylen)
        return self.SendCommand

    def UnpackResponse(self, Response):
        # Unpack Response Header and store in every field.
        self.RecvUnused, self.RecvCmdid,\
            self.RecvGroupid, self.RecvVersion,\
            self.RecvPaylen, self.ResultCode,\
            self.ResultMsg = unpack_from(
                self.ResponseHeaderFormat, Response, offset=0)
        self.ResultMsg = self.ResultMsg.decode().rstrip('\x00')
        return self.RecvUnused, self.RecvCmdid, self.RecvGroupid, self.RecvVersion,\
            self.RecvPaylen
    
    def ReturnCheck(self):
        return self.ResultCode, self.ResultMsg

    def STDOut(self):
        # Print out every fields individually.
        # Note: Need to decode content, if the type of field is char as ResultMsg.
        self.logger.debug("UNUSED: " + str(self.RecvUnused))
        self.logger.debug("CMDID: " + str(self.RecvCmdid))
        self.logger.debug("GRPID: " + str(self.RecvGroupid))
        self.logger.debug("VSION: " + str(self.RecvVersion))
        self.logger.debug("GRPID: " + str(self.RecvGroupid))
        self.logger.debug("PAYLEN: " + str(self.RecvPaylen))
        self.logger.info("ResultCode: " + str(self.ResultCode))
        self.logger.info("ResultMsg: " + repr(self.ResultMsg))
