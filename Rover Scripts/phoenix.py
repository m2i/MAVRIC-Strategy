import math
import socket
import threading

class Phoenix (threading.Thread):
    _temperature_socket = None
    _actuator_socket = None
    _run = True
    _temperature = 0.;
    _actuator = 0.;
    _gps = None
    _ip = None
    
    def __init__(self, ip):
        self._gps = GPS(ip, 8001);
        self._ip = ip
        threading.Thread.__init__(self)
        
    def run(self):
        self._gps.start()
        temperature_buffer = ''
        actuator_buffer = ''
        while self._run:
            try:
                if self._temperature_socket == None:
                    self._temperature_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self._temperature_socket.settimeout(1)
                    self._temperature_socket.connect((self._ip, 8002))
                temperature_buffer = temperature_buffer + self._temperature_socket.recv(1024).decode()
                while '\r\n' in temperature_buffer:
                    (line, temperature_buffer) = temperature_buffer.split('\r\n', 1)
                    self._temperature = float(line)
                                    
            except socket.error as e:
                print(e)
                self._temperature_socket = None
            
            try:
                if self._actuator_socket == None:
                    self._actuator_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self._actuator_socket.settimeout(1)
                    self._actuator_socket.connect((self._ip, 10002))
                actuator_buffer = actuator_buffer + self._actuator_socket.recv(1024).decode()
                while '\r\n' in actuator_buffer:
                    (line, actuator_buffer) = actuator_buffer.split('\r\n', 1)
                    self._actuator = float(line)
                
            except socket.error as e:
                print(e)
                self._actuator_socket = None
                
    def close(self):
        self._run = False
        self._gps.close()
        self.join()
        self._temperature_socket.close()
        
    def setWheels(self, left, right):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((self._ip, 9002))
            s.sendall(('D'+str(left)+','+str(right)).encode())
            s.close()
        except socket.error as e:
            print(e)
            
    def setActuator(self, direction):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((self._ip, 10001))
            s.sendall(('FSR'[direction+1]).encode())
            s.close()
        except socket.error as e:
            print(e)

    @property
    def temperature(self):
        return self._temperature
    
    @property
    def actuator(self):
        return self._actuator
    
    @property
    def gps(self):
        return self._gps
    
class GPS (threading.Thread):
    _good_fix = False
    _latitude = 0.
    _longitude = 0.
    _altitude = 0.
    _speed = 0.
    _heading = 0.
    _satelites = 0.
    _ip = None
    _port = None
    _socket = None
    _run = True
    
    def __init__(self, ip, port):
        self._ip = ip
        self._port = port
        threading.Thread.__init__(self)
        
    def parseLine(self, line):
        data = line.split(',')
        self._good_fix = bool(data[0])
        self._latitude = float(data[1])
        self._longitude = float(data[2])
        self._altitude = float(data[3])
        self._speed = float(data[4])
        self._heading = float(data[5])
        self._satellites = int(data[6])
        
    def run(self):
        buffer = ''
        while self._run:
            try:
                if self._socket == None:
                    self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self._socket.settimeout(1)
                    self._socket.connect((self._ip, self._port))
                buffer = buffer + self._socket.recv(1024).decode()
                while "\n" in buffer:
                    (line, buffer) = buffer.split('\n', 1)
                    self.parseLine(line)
            except socket.error as e:
                self._socket = None

    def close(self):
        self._run = False
        self.join()
        self._socket.close()

    @property
    def good_fix(self):
        return self._good_fix
    
    @property
    def latitude(self):
        return self._latitude
    @property
    def longitude(self):
        return self._longitude

    @property
    def altitude(self):
        return self._altitude

    @property
    def speed(self):
        return self._speed
        
    @property
    def heading(self):
        return self._heading

    @property
    def satellites(self):
        return self._satellites