import RPi.GPIO as gpio
import time

class Raspi_Com:

    def __init__(self):
        
        self.output_pin_1 = 3
        self.output_pin_2 = 5

        self.output_pin_1 = 11
        self.output_pin_2 = 13

        self.setup_communication()

        self.read_message_dict = dict()
        self.write_message_dict = dict()

        self.read_string = ""
        self.write_string = ""
    
    def setup_read_message_dict(self):
        self.read_message_dict["00"] = "Motors_Stop"
        self.read_message_dict["01"] = "Motors_Forward"
        self.read_message_dict["10"] = "Motors_Backward"
        self.read_message_dict["11"] = "Wait_Raspberry"

        self.write_message_dict["Motors_Stop"]  = "00"
        self.write_message_dict["Motors_Start"] = "01"


    def setup_communication(self):
        gpio.setwarnings(False)
        gpio.setmode(gpio.BOARD)

        gpio.setup(self.output_pin_1, gpio.OUT)
        gpio.setup(self.output_pin_2, gpio.OUT)

        gpio.setup(self.input_pin_1, gpio.IN)
        gpio.setup(self.input_pin_2, gpio.IN)

    def set_write_string(self, message):

        if self.write_message_dict[message] == "00":
            gpio.output(self.output_pin_1, gpio.LOW)
            gpio.output(self.output_pin_2, gpio.LOW)
        
        elif self.write_message_dict[message] == "01":
            gpio.output(self.output_pin_1, gpio.LOW)
            gpio.output(self.output_pin_2, gpio.HIGH)

        else:
            print("wrong change.! your change must be available option. your change is {}".format(message))
    
    def read_arduino(self):
        while True:
            self.input_pin_1_read = str(gpio.input(self.input_pin_1))
            self.input_pin_2_read = str(gpio.input(self.input_pin_2))


