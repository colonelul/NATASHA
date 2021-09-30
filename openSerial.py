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
import io
import time
import cv2

global serial_object

devices_ids = {'CH340': {'VID': '1A86', 'PID': '7523'}}

"""Activate debug mode!"""
debug = False

def device_port(devicess):
    device_list = list_ports.comports()

    for device in device_list:
        if (device.vid != None or device.pid != None):
            if ('{:04X}'.format(device.vid) == devices_ids[devicess]['VID'] and '{:04X}'.format(device.pid) == devices_ids[devicess]['PID']):
                port = device.device
                return port
            port = None

def connect():
    global serial_object
    portt = device_port('CH340')
    try:
        if debug:
            print("Trying to connect -> " + str(portt))
        
        serial_object = serial.Serial(
            port = portt,                   #select port!
            baudrate = 9600,                #select boudrate!
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout = 0.5
        )
    except:
        print("Failed to connect on " + str(portt))

def get_data():
    global serial_object
    data_receive = None
    try:
        if serial_object.inWaiting() > 0:
            data_receive = serial_object.readline(serial_object.inWaiting()).hex()
    except:
        if debug: print("Data received is NUll!")
        else: pass
    if data_receive != None and debug:
        print("DATA_RECEIVED-> " + data_receive)
        
    return data_receive

def send(data):
    global serial_object
    try:
        serial_object.write(data)
        if debug: print('DATA_SEND-> ' + str(data)) 
    except:
        if debug: print("Send data not working!") 
        else: pass
    







