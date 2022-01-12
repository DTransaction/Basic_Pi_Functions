import os
import glob
import time
import RPi.GPIO as GPIO



# General Setup
pins = [16]
GPIO.setmode(GPIO.BCM) #sets how we reference GPIO pins
GPIO.setup(pins, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #set GPIO pins

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_path = glob.glob(base_dir + '28*')[0] # Get file path of sensor

# Function definitions
def read_temp_raw():
    with open(device_path +'/w1_slave','r') as f:
        print(f)
        # valid, temp = f.readlines()
read_temp_raw()
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
