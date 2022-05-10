import serial
import time

class Arduino_communication():
    
    def __init__(self):
        self.arduino = None
        self.port = None
        self.init()

    def init(self):
        self.port, self.arduino = self.com_arduino_searcher()

    def com_arduino_searcher(self):
        arduino = None
        port = None

        for com_number in range(10):
            port = 'COM' + str(com_number)
            try: 
                arduino = serial.Serial(port=port, baudrate=9600)
                if (arduino is not None):
                    print("[DEBUG]: Arduino Port: {}".format(port))
            except serial.serialutil.SerialException:
                continue
        if arduino == None:
            print("[WARNING]: Arduino port is not found.!")
            
        return port,arduino

    def read_data_from_arduino(self):
        return self.arduino.readline()

    def send_data_to_arduino(self, sended_data):
        self.arduino.write(bytes(sended_data, 'utf-8'))
        time.sleep(0.05)

a = Arduino_communication()
a.send_data_to_arduino("1")

print(a.read_data_from_arduino())

