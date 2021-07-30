import os
import csv
import serial
from serial.tools import list_ports
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
        self.ser = self.init_serial(self.port, self.baudrate, self.timeout)#, dsrdtr=True)
        if self.ser:
            self.__init_ready()
    
    def init_serial(self, port=None, baudrate=None, timeout=None):
        if port is None:
            port = self.port
        if baudrate is None:
            baudrate = self.baudrate
        if timeout is None:
            timeout = self.timeout
        try:
            self.ser = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
        except Exception as e:
            print(e, 'no arduino')
            self.ser = None
    
    def __init_ready(self):
        while True:
            msg = self.ser.readline()
            if msg == b'arduino is avairable\n':
                break
    
    def receive(self):
        data = self.ser.readline()
        try:
            data = data.decode('utf-8').replace('\n', '').split(',')
            data = list(map(int, data))
        except Exception as e:
            data = None
        return data
    
    def __record(self, data):
        self.raw[-1].append(data)
        self.data_queue.put(data)
    
    def start(self, runtime=None):
        if self.is_running:
            return False
        self.raw.append([])
        self.ser.write(b'1')
        self.is_running = True
        t, *v = self.receive()
        self.columns = ['time', *[f'data{n}' for n in range(len(v))]]
        self.__record([t, *v])
        self.start_time = int(t)
        self.thread = Thread(target=self.run, args=(runtime, ), daemon=True)
        self.thread.start()
        return True

    def run(self, runtime=None):
        while self.is_running:
            data = self.receive()
            if not data is None:
                if data[0] > runtime * 1000: # ms
                    # TODO 以下2行の処理はself.stopと被る部分があるからどーにかする
                    self.is_running = False
                    self.ser.write(b'0')
                self.__record(data)

    def stop(self):
        if self.is_running:
            self.is_running = False
            self.ser.write(b'0')
            self.thread.join()
            return True
        return False
    
    def open(self):
        if not self.ser.is_open:
            self.ser.open()
    
    def close(self):
        if self.ser.is_open:
            self.ser.close()
            
    def save(self, n=-1, path='./', fname='arduino.csv'):
        try:
            if fname[-4:] != '.csv':
                fname += '.csv'            
            with open(path+fname, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(self.columns)
                writer.writerows(self.raw[n])
        except Exception as e:
            print(e)
            return False
    
    @staticmethod
    def get_comports():
        ports = []
        for cp in list_ports.comports():
            ports.append(cp.description)
        return ports
