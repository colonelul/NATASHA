import serial

class SerialConnection:
    def __init__(self):
        self.serial_object = None
        self.__connect__()
    
    def __connect__(self):
        try:
            '''~~Comunicare Serial pentru PC~~
                 serial_object.port = 'COM?' -> ?: numarul portului de comunicare'''
            
            with serial.Serial() as self.serial_object:
                self.serial_object = 9600
                self.serial_object.port = 'COM1' #selectare port 
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
        while(1):
            try:
                filter_data = self.serial_object.readline()
                self.filter_data_decode = filter_data.decode('utf-8')
            except:
                pass
            
            print("DATA_RECEIVED-> " + self.filter_data_decode)
            return self.filter_data_decode
    
    def send(self, data):
        self.send_data = data
        print('DATA_SEND-> ' + self.send_data)
        self.serial_object.write(self.send_data.encode())
    
            