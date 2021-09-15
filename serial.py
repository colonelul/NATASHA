import serial

class SerialConnection:
    def __init__(self):
        self.serial_object = None
    
    def __connect__(self):
        self.locations=['/dev/ttyUSB0', '/dev/ttyUSB1']
        
        for device in self.locations:
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
            print(self.filter_data_decode)
    
    def send(self, data):
        self.send_data = data
        print('DATA-SEND-> ' + self.send_data)
        self.serial_object.write(self.send_data.encode())