# Import statements
import os
import glob
import time
import RPi.GPIO as GPIO



# General Setup
pins = [16]
GPIO.setmode(GPIO.BCM)
GPIO.setup(pins, GPIO.OUT)

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_path = glob.glob(base_dir + '28*')[0] # Get file path of sensor

# Function definitions
def ledON():
    GPIO.output(pins[0], GPIO.HIGH)

def ledOFF():
    GPIO.output(pins[0], GPIO.LOW)

try:
    while True:
        with open(device_path + '/w1_slave', 'r') as f:
            temp = int((str(f.readlines()))[76:81])/1000
        print(temp)
        if temp >= 20 and temp <= 25:
            ledON()
            print("READY")
        elif GPIO.input(pins[0]) == 1:
            ledOFF()
        time.sleep(1)

except:
    GPIO.cleanup()
