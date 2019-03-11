'''
=======================================================================
                        Interface of ConnectionType
=======================================================================
A ConnectionType interface for TestPC to select what kind of type to
communicate with target device. Before creating TestPC object, create
ConnctionType object first.
1. SocketMethod
   Input: device IP and Port.
2. SerialMethod
   Not ready.
3. SSHMethod
   Not ready.
=======================================================================
'''
import abc


class ConnectionType(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def Connect(self):
        #Connect to target device.
        pass

    @abc.abstractmethod
    def Send(self, cmd):
        #Send command to target device.
        pass
 
    @abc.abstractmethod
    def Receive(self):
        #Recive Response from target device.
        pass

    @abc.abstractmethod
    def Disconnect(self):
        #DisConnect Test PC and target device.
        pass




