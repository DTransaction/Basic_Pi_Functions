import time
import RPi.GPIO as GPIO

#General Setup
def button_callback(count):
    print(count)
    count += 1

GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
pin = 8
count = 0

GPIO.setwarnings(False)
GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set to be an input pin and set initial value to be pulled low (off)
GPIO.add_event_detect(pin, GPIO.RISING, callback=button_callback(count)) 

message = input("Press enter to quit\n\n") # Run until someone presses enter

GPIO.cleanup() # Clean up