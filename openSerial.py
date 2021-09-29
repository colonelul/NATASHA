""" Comunicare cu laserul (LST-25/JIB) pentru a obtine date de la dansul 
    bite 1 -> 1
    bite 2 -> 3
    bite 3 -> 0
    bite 4 -> 97 
    bite 5 -> 0
    bite 6 -> 1
    bite 7 -> 213
    bite 8 -> 212 """


import serial

class SerialConnection:
    def __init__(self):
        self.serial_object = None
    
    def __connect__(self):
        try:
            '''~~Comunicare Serial pentru PC~~
                 serial_object.port = 'COM?' -> ?: numarul portului de comunicare'''
            
            print("Trying to connect(PC)")
            
            with serial.Serial() as self.serial_object:
                self.serial_object.boudrate = 9600
                self.serial_object.port = 'COM26' #selectare port 
                self.serial_object.open()
            
        except:
            '''comunicare Serial pentru RASPBERRY'''
            
            locations=['/dev/ttyUSB0', '/dev/ttyUSB1']
            
            for device in locations:
                try:
                    print("Trying..." + device)
                    self.serial_object = serial.Serial(device, 9600)
                    
                    break
                except:
                    print("Failed to connet on" + device)
        
    def get_data(self):
        filter_data_decode = ""
        while(1):
            try:
                filter_data = self.serial_object.readline()
                filter_data_decode = filter_data.decode('utf-8')
            except:
                print("Data received is NUll!")
                
            if filter_data_decode != "":
                print("DATA_RECEIVED-> " + filter_data_decode)
            return filter_data_decode
    
    def send(self, data):
        send_data = data
        
        try:
            self.serial_object.write(self.send_data.encode())
            print('DATA_SEND-> ' + send_data)
        except:
            print("Send data not working!")
    
    def send_to_laser(self):
        values = bytearray([1, 3, 0, 97, 0, 1, 213, 212])
        self.serial_object.write(values)

SerialConnection().__connect__()












