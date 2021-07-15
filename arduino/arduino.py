import os
import serial
import queue
from threading import Thread


class Arduino:
    def __init__(self) -> None:
        self.raw = []
        self.start_time = None
        self.is_running = False
        self.thread = None
        self.data_queue = queue.Queue()

        self.port = 'COM6' if os.name == 'nt' else '/dev/ttyACM0'
        self.baudrate = 115200
        self.timeout = 0.5
        self.serial = serial.Serial(self.port, self.baudrate, timeout=self.timeout)#, dsrdtr=True)
        self.__init_ready()
    
    def __init_ready(self):
        while True:
            msg = self.serial.readline()
            if msg == b'arduino is avairable\n':
                break
    
    def receive(self):
        data = self.serial.readline()
        try:
            data = data.decode('utf-8').replace('\n', '').split(',')
            data = list(map(int, data))
        except Exception as e:
            data = None
        return data
    
    def __record(self, data):
        self.raw[-1].append(data)
        self.data_queue.put(data)
    
    def start(self):
        self.raw.append([])
        self.serial.write(b'1')
        self.is_running = True
        t, *v = self.receive()
        self.__record([t, *v])
        self.start_time = int(t)
        self.thread = Thread(target=self.run, daemon=True)
        self.thread.start()

    def run(self):
        while self.is_running:
            data = self.receive()
            self.__record(data)

    def stop(self):
        self.is_running = False
        self.serial.write(b'0')
        self.thread.join()

    def open(self):
        if not self.serial.is_open():
            self.serial.open()
    
    def close(self):
        if self.serial.is_open():
            self.serial.close()