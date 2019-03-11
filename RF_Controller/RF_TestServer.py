import socket

HOST = '127.0.0.1'       # Symbolic name meaning all available interfaces
PORT = 5025              # Arbitrary non-privileged port

try:
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen(1)
            print('======= Test Socket Server =======')
            print('Server IP:', HOST)
            print('Press Ctrl + break to exit...')
            print('wait for connection...')
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                while True:
                    data = conn.recv(1024)
                    if not data: 
                        break
                    print('Receive: ', data.decode())
                    conn.sendall("Server received you message: {0}".format(data.decode()).encode())
except KeyboardInterrupt:
    print('interrupted!')