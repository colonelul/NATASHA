""" Comunicare cu laserul (LST-25/JIB) pentru a obtine date de la dansul 
    bite 1 -> 1
    bite 2 -> 3
    bite 3 -> 0
    bite 4 -> 97 
    bite 5 -> 0
    bite 6 -> 1
    bite 7 -> 213
    bite 8 -> 212 
    
   ~~PENTRU CH340 -> VID_1A86 PID_7523"""

from serial.tools import list_ports
import serial

class SerialConnection:
    def __init__(self):
        self.devices_ids = {'CH340': {'VID': '1A86', 'PID': '7523'},
                            'CAMERA': {'VID': '?', 'PID': '?'}}
        self.__connect__()
    
    def device_port(self, devicess):
        device_list = list_ports.comports()

        for device in device_list:
            if (device.vid != None or device.pid != None):
                if ('{:04X}'.format(device.vid) == self.devices_ids[devicess]['VID'] and '{:04X}'.format(device.pid) == self.devices_ids[devicess]['PID']):
                    port = device.device
                    return port
                port = None
    
    def __connect__(self):
        portt = self.device_port('CH340')
        try:
            print("Trying to connect -> " + portt)
            
            SERIAL_OBJECT = serial.Serial(
                port = portt,                   #select port!
                baudrate = 9600,                #select boudrate!
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout = 0.5
            )
        except:
            print("Failed to connect on " + portt)

class Connection(SerialConnection):
    def get_data(self):
        filter_data = None
        try:
            filter_data = self.SERIAL_OBJECT.readline().hex()
        except:
            print("Data received is NUll!")
            
        if filter_data != None:
            print("DATA_RECEIVED-> " + filter_data)
            
        return filter_data
    
    def send(self, data):
        try:
            self.SERIAL_OBJECT.write(data)
            print('DATA_SEND-> ' + str(data))
        except:
            print("Send data not working!")












