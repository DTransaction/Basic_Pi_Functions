import time
import RPi.GPIO as GPIO

print("Setup") #informs user setup has begun

#General Setup
pins = [18]
GPIO.setmode(GPIO.BCM) #sets how we reference GPIO pins
GPIO.setup(pins, GPIO.OUT) #sets GPIO pin 23 as an output

#PWM Signal Setup
pin = GPIO.PWM(pins[0],50) #set pin 23 as a PWM output, with a frequency of 50 Hz
pin.start(0) #sets the starting duty cycle of the PWM signal to 0% and initializes the signal
time.sleep(1) #sleep for a second to ensure signal is initialized properly

print("Begin") #informs user the main function of the program is beginning

#Main portion of program
try:
    for cycle in range(100):
            pin.ChangeDutyCycle(cycle) #changes the duty cycle
            time.sleep(0.1) #sleeps for 2 seconds

except KeyboardInterrupt: #stops try if (ctrl + c) is pressed
    pass

print("Done") #informs the user the program is finished running

pin.stop() #stops the pin initialization
GPIO.cleanup() #cleansup all of the GPIO pins used within the script
