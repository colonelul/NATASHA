import serial
import serial.rs485

ser = serial.Serial('COM26', 9600, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)

values = bytearray([1, 3, 0, 97, 0, 1, 213, 212])
ser.write(values)

filter_data = ser.readline()
print(filter_data)



