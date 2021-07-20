import time
import socket
import pickle
from configparser import ConfigParser

class MySocket:
    def __init__(self, sock=None) -> None:
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock
        #self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.is_running = False
        
    def init_server(self, host, port, bind=5):
        self.sock.bind((host, port))
        self.sock.listen(bind)
        
    def accept(self):
        client, address = self.sock.accept()
        return client, address

    def connect(self, host, port):
        try:
            self.sock.connect((host, port))
            return True
        except socket.error as e:
            raise Exception(e)
            return False

    def send(self, data):
        data = pickle.dumps(data)
        try:
            self.sock.send(data)
            return True
        except socket.error as e:
            return False
        
    def receive(self):
        data = b''
        try:
            while True:
                tmp, address = self.sock.recv(2**12)
                if len(tmp) <=0:
                    break
                data += tmp
            data = pickle.loads(data)
        except Exception as e:
            raise Exception(e)
        else:
            return data
    
    
    
def server_process():
    HOST = socket.gethostbyname(socket.gethostname())
    PORT = 12345
    s = MySocket()
    s.init_server(HOST, PORT)
    while True:
        try:
            print('Waiting client')
            client, address = s.accept()
            print(f'Connect to {address}')
            msg = s.receive()
            print(f'> {msg}  (from {address})')
        except KeyboardInterrupt as e:
            print('Ctrl-C is pressed')
            client.close()
            break
        
def client_process():
    HOST = socket.gethostbyname(socket.gethostname())
    PORT = 12345
    s = MySocket()
    while True:
        try:
            s.connect(HOST, PORT)
            msg = input('< ')
            s.send(msg)
        except KeyboardInterrupt as e:
            print('Ctrl- is pressed')
            break
    
def main():
    import sys
    if sys.argv[1] == 's':
        server_process()
    elif sys.argv[1] == 'c':
        client_process()
    
    
if __name__ == '__main__':
    main()