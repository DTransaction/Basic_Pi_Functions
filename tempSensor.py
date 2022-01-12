# Import statements
import os
import glob
import time
import RPi.GPIO as GPIO



# General Setup
pins = [16]
GPIO.setmode(GPIO.BCM)
GPIO.setup(pins, GPIO.OUT)

# os.system('modprobe w1-gpio')
# os.system('modprobe w1-therm')

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
        # valid, temp = f.readlines()

#     return valid, temp
 
# def read_temp():
#     valid, temp = read_temp_raw()

#     while 'YES' not in valid:
#         time.sleep(0.2)
#         valid, temp = read_temp_raw()

#     pos = temp.index('t=')
#     if pos != -1:
#         #read the temperature .
#         temp_string = temp[pos+2:]
#         temp_c = float(temp_string)/1000.0 
#         temp_f = temp_c * (9.0 / 5.0) + 32.0
#         return temp_c, temp_f
 
# print(' ROM: '+ rom)

# while True:
#     c, f = read_temp()
#     print('C={:,.3f} F={:,.3f}'.format(c, f))
#     time.sleep(1)
