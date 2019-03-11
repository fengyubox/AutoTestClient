'''
================================================================
                        SSHConnection
================================================================
The class implement how to communicate with target device by
SSH with IP and Port of target device. There are four
function as below.
Function:
1. Connect():    Open the SSH of client to connect to server
                 which is on target device.

2. Send():       Send suitable command which is an input to
                 target device.

3. Receive():    Receive corresponding response from targe device,
                 after sending command. Input a response length
                 to predefine how many bytes for buffer should
                 be reserve.

4. Disconnect(): Close the SSH of client to disconnect to
                 server which is on target device.

Input of creating object: IP and Port of target device.
Ex: ConnectionType = SSHConnection("192.168.84.1",7654)
================================================================
'''
import paramiko
from sshtunnel import SSHTunnelForwarder


class SSHConnection(object):

    def __init__(self):
        self.Tunnel().start()
        self.Connect()
    
    def Tunnel(self):
        tunnel = SSHTunnelForwarder(
           ('210.200.12.18', 22),
            ssh_username='richard_wen',
            ssh_password='richard123',
            remote_bind_address=('10.35.65.54', 22),
            local_bind_address=('0.0.0.0', 10022) 
        )
        return tunnel

    def Connect(self):
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #set banner timeout 
        #transport = paramiko.Transport((self.host, self.port))
        #print(transport.banner_timeout)
        #transport.banner_timeout = 30
        #print(transport.banner_timeout)
        self.client.connect(
            hostname='127.0.0.1',
            port=10022,
            username='wistron',
            password='Welc0me',
            timeout=10,
            allow_agent=False,
            look_for_keys=False
        )
        
    def Send(self, command):
        '''Send and execute command'''
        stdin, stdout, stderr = self.client.exec_command(command, timeout=10)
        self.stdout = stdout.read()
        self.stderr = stderr.read()

    def Receive(self):
        '''Receive result from DUT'''
        return self.stdout, self.stderr

    def Disconnect(self):
        '''Close SSH client'''
        self.client.close()
        self.Tunnel().close()
        self.client = None

if __name__ == "__main__":
    ssh = SSHConnection()
    ssh.Send('uname -a')
    print(ssh.Receive())
    ssh.Disconnect()