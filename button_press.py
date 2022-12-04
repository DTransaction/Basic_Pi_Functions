import time
import RPi.GPIO as GPIO

#General Setup
def button_callback(channel):
    print(count)

GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
pin = [8]

GPIO.setwarnings(False)
GPIO.setup(pin[0], GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set to be an input pin and set initial value to be pulled low (off)
GPIO.add_event_detect(pin[0],GPIO.RISING,callback=button_callback) # Setup event on pin rising edge

count = 0
message = input("Press enter to quit\n\n") # Run until someone presses enter


GPIO.cleanup() # Clean up