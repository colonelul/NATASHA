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
            