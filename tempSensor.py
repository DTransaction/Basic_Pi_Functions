# Import statements
import os
import glob
import time
import RPi.GPIO as GPIO



# General Setup
pins = [16] # Initializes the GPIO pin of the LED
GPIO.setmode(GPIO.BCM)
GPIO.setup(pins, GPIO.OUT)

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_path = glob.glob(base_dir + '28*')[0] # Gets the file path of sensor



# Function definitions
def ledON() -> None:
    """
    Sets the GPIO pin voltage to 3.3V, turning on the LED
    """
    GPIO.output(pins[0], GPIO.HIGH)

def ledOFF() -> None:
    """
    Sets the GPIO pin voltage to 0V, turning off the LED
    """
    GPIO.output(pins[0], GPIO.LOW)

def getTemp() -> int:
    """
    Returns the temperature value from the sensor in celcius
    """
    with open(device_path + '/w1_slave', 'r') as f:
        temp = int((str(f.readlines()))[76:81])/1000 # Extracts the temperature value 
    return temp

def repeatedGetTemp(): 
    while True:
        tempC = getTemp()
        print(f"{tempC}C")
        time.sleep(1) 

def findTempRange(range: list) -> None:
    """
    Flashes LED when temperature gets between provided range (list with two int elements), and is solid when within 5 degrees celcius of the limits
    """
    lower, upper = range[0], range[1]
    softLower, softUpper = lower - 5, upper + 5
    while True:
        tempC = getTemp()
        print(tempC)
        if tempC >= softLower and tempC <= softUpper:
            ledON()
            print("ALMOST")
        elif tempC >= lower and tempC <= upper:
            for x in range(5):
                ledOFF()
                time.sleep(0.5)
                ledON()
                time.sleep(0.5)
        elif GPIO.input(pins[0]) == 1:
            ledOFF()
        time.sleep(1)



# Main script

coffee = [60, 70] # Constant temperature ranges
tea = [55, 65]

menuCommands = {1: repeatedGetTemp, 2: findTempRange(coffee), 3: findTempRange(tea), 4: findTempRange([int(input("Lower limit\n> ")), int(input("Upper limit\n> "))])}
menuPrompt = "1 - Constantly read temperature\n2 - Optimal temperature for coffee\n3 - Optimal temperature for tea\n4 - Set custom temperature ranges\nCTRL + C to quit any process\n> "

try: # Allows user to CTRL + C out of the program and properly clean up GPIO pin
    user = int(input(menuPrompt))
    command = menuCommands.get(user)
except:
    GPIO.cleanup()
