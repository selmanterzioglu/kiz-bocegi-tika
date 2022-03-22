import RPi.GPIO as gpio
import time

gpio.setwarnings(False)

output_pin_1 = 3
output_pin_2 = 5

input_pin_1 = 11
input_pin_2 = 13

gpio.setmode(gpio.BOARD)

gpio.setup(output_pin_1, gpio.OUT)
gpio.setup(output_pin_2, gpio.OUT)

gpio.setup(input_pin_1, gpio.IN)
gpio.setup(input_pin_2, gpio.IN)


while True:
    
    input_pin_1_read = gpio.input(input_pin_1)
    input_pin_2_read = gpio.input(input_pin_2)
        
    gpio.output(output_pin_1, gpio.LOW)
    gpio.output(output_pin_2, gpio.LOW)

    
    print("""
        input_1: {} input_2: {}""".format(str(input_pin_1_read), str(input_pin_2_read) )
    
    )
