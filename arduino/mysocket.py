import configparser
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
        self.clients = []
        self.is_running = False
        
    def init_server(self, host, port, bind=5):
        self.sock.bind((host, port))
        self.sock.listen(bind)
        
    def accept(self):
        client, address = self.sock.accept()
        self.clients.append((client, address))
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
        
    def receive(self, n=-1):
        client = self.clients[n][0]
        data = b''
        try:
            while True:
                tmp, address = self.client.recv(2**12)
                if len(tmp) <=0:
                    break
                data += tmp
            data = pickle.loads(data)
        except Exception as e:
            raise Exception(e)
        else:
            return data
    
    
    
def server_process(host, port):
    HOST = host
    PORT = port
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
        
def client_process(host, port):
    HOST = host
    PORT = port
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
    conf = ConfigParser()
    conf.read('./config/connection.conf')
    sock_info = input(conf.sections())
    host = conf[sock_info]['ip']
    port = int(conf[sock_info]['port'])
    print(host, port)
    if sys.argv[1] == 's':
        server_process(host, port)
    elif sys.argv[1] == 'c':
        client_process(host, port)
    
    
if __name__ == '__main__':
    main()