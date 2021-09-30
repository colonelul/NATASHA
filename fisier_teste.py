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
from imutils import perspective
from scipy.spatial import distance as dist


def midpoint(ptA, ptB):
        return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

img = cv2.imread(imgg)

x=400
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

cc = [[],[]]

cc[0] = cnts[0]
cc[1] = cnts[2]

for c in cc:
    
    orig = img.copy()
    
    box = cv2.minAreaRect(cc[0])
    box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
    box = perspective.order_points(box)
    cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)

    for (x, y) in box:
        cv2.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)
    
    
    (tl, tr, br, bl) = box
    (tltrX, tltrY) = midpoint(tl, tr)
    (blbrX, blbrY) = midpoint(bl, br)
    
    cv2.circle(orig, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
    cv2.circle(orig, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
    
    cv2.line(orig, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),
    		(255, 0, 255), 2)
    
    dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
    
    dimA = dA / pixelsPermm
    
    cv2.putText(orig, "{:.1f}mm".format(dimA),
    		(int(tltrX - 15), int(tltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX,
    		0.65, (255, 255, 255), 2)
    
    cv2.imshow("Image", orig)
    cv2.waitKey(0)
    
    print(dimA)
    

cv2.imshow("3-erode", edged)
cv2.waitKey(0)














