import serial
serial_object = None

ser = serial.Serial(
    port='COM26',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=0.5
)

values = bytearray(b'\x01\x03\x00a\x00\x01\xd5\xd4')

while True:
    ser.write(values)
    data = ser.readline().hex()
    data = data[6:10]
    print(float.fromhex(data)*0.001)





from serial.tools import list_ports
""" PENTRU CH340 -> VID_1A86 PID_7523"""

VID = "1A86"
PID = "7523"

device_list = list_ports.comports()

for device in device_list:
    if (device.vid != None or device.pid != None):
        if ('{:04X}'.format(device.vid) == VID and
            '{:04X}'.format(device.pid) == PID):
            port = device.device
            break
        port = None

print(port)


devices_ids = {'CH340': {'VID': '1A86', 'PID': '7523'},
               'CAMERA': {'VID': '?', 'PID': '?'}}

devices_ids['CH340']['VID']