import socket
from configparser import ConfigParser

class MySocket:
    def __init__(self, sock=None) -> None:
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.is_running = False

    def connect(self, host, port):
        try:
            self.sock.connect((host, port))
            return True
        except socket.error as e:
            return False

    def send(self, data):
        try:
            self.sock.send(data.encode('utf-8'))
            return True
        except socket.error as e:
            return False
        
    def receive(self):
        data = b''
        try:
            while True:
                tmp = self.sock.recv(1024).decode('utf-8')
                if len(tmp) <=0:
                    break
                data += tmp
        except Exception as e:
            raise Exception(e)
        else:
            return data
        finally:
            return None
    