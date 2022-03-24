
import time
import libs
import logging
from structure_threading import Thread_Object


class RPI_Communication():

    def __init__(self, logger_level=logging.INFO, test_mode = False):
        
        self.logger = logging.getLogger("RPI_Communication")

        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '[%(asctime)s][%(levelname)s] %(name)s : %(message)s',
            "%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logger_level)

        self.output_pin_1 = 3
        self.output_pin_2 = 5

        self.input_pin_1 = 11
        self.input_pin_2 = 13

        self.read_message_dict = dict()
        self.write_message_dict = dict()    
        self.__thread_Dict = dict()

        self.read_message  = ""
        self.write_message = ""
        self.input_pin_1_read = ""
        self.input_pin_2_read = ""
        
        self.test_mode = test_mode

        self.init()
        
    def init(self):        
        self.setup_read_message_dict()
        if not self.is_test_mode:
            self.setup_communication()
        
    def setup_read_message_dict(self):
        self.read_message_dict["00"] = "Motors_Stop"
        self.read_message_dict["01"] = "Motors_Forward"
        self.read_message_dict["10"] = "Motors_Backward"
        self.read_message_dict["11"] = "Wait_Raspberry"
        {
            "KEY": "VALUE",
            "KEY": "VALUE",
            "KEY": "VALUE"
        }
        self.write_message_dict["Motors_Stop"]  = "00"
        self.write_message_dict["Motors_Start"] = "01"

    def thread_read_arduino(self, trigger_quit=None):
        self.__thread_Dict["main_Thread"] = Thread_Object(
            name="RPI_Communication.thread_read_arduino",
            delay=0.0001,
            logger_level=self.logger.getEffectiveLevel(),
            set_Deamon=True,
            run_number=None,
            quit_trigger=trigger_quit
        )
        self.__thread_Dict["main_Thread"].init(
            task=self.read_arduino
        )
        self.__thread_Dict["main_Thread"].start()


    def setup_communication(self):
        import RPi.GPIO as gpio
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

        if self.is_test_mode:
            while True:
                self.read_message = self.read_message_dict[self.input_pin_1_read + self.input_pin_2_read]
                print("read_message: ", self.read_message)
        else:
            while True:
                self.input_pin_1_read = str(gpio.input(self.input_pin_1))
                self.input_pin_2_read = str(gpio.input(self.input_pin_2))
                self.read_message = self.read_message_dict[self.input_pin_1_read + self.input_pin_2_read]

    def set_test_mode(self, bool):
        self.test_mode = bool
    
    def is_test_mode(self):
        return self.test_mode
        

if __name__ == "__main__":
    test = RPI_Communication(test_mode=True)
    test.input_pin_1_read = "0"
    test.input_pin_2_read = "1"
    test.thread_read_arduino(trigger_quit=None)
    

