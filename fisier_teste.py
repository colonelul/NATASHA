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


imgg = 'Z:/NATASHA/Camera/1.jpg'

import cv2
import numpy as np
import imutils
from scipy.stats import linregress
from scipy.spatial import distance

img = cv2.imread(imgg)

x=0 
y=500
h=250
w=1200

pixelsPermm = 0.035
img = img[y:y+h, x:x+w]

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (7, 7), 0)
edged = cv2.Canny(gray, 120, 200)
edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)

cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key=cv2.contourArea, reverse=False)[:5]

cc = [[],[]]
cc[0] = cnts[2]
cc[1] = cnts[1]

a = np.empty(len(cc[0]))
b = np.empty(len(cc[0]))

for i in range(len(cc[0])):
    a[i] = cc[0][i][0][1]
    b[i] = cc[1][i][0][1]

m = a - b

print(m[0]*pixelsPermm)
print(m[-1]*pixelsPermm)
print(m[int(len(m)/2)]*pixelsPermm)

cv2.imshow("Image", edged)
if cv2.waitKey(0) & 0xFF == ord('q'): 
    cv2.destroyAllWindows()

b = '010302457'

b[:2]

devices_adress = {'laser': '01', 'hault': '02', 'motor_natasha': '03'}

devices_adress['laser']

































