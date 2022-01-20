# Import statements
import os
import glob
import time
import RPi.GPIO as GPIO
import yagmail
from bs4 import BeautifulSoup
import requests
import shutil


# General Setup
pins = [16] # Initializes the GPIO pin of the LED
GPIO.setmode(GPIO.BCM)
GPIO.setup(pins, GPIO.OUT)
GPIO.setwarnings(False)

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_path = glob.glob(base_dir + '28*')[0] # Gets the file path of sensor



# Function definitions
def LED_on(): GPIO.output(pins[0], GPIO.HIGH)

def LED_off(): GPIO.output(pins[0], GPIO.LOW)

def get_temp() -> int:
    with open(device_path + '/w1_slave', 'r') as f:
        temp = int((str(f.readlines()))[76:81])/1000
    return temp

def repeated_get_temp(): 
    try:
        LED_on()
        while True:
            temp = get_temp()
            print(f"{temp} C")
            time.sleep(1) 
    except: 
        LED_off()

def find_temp_range(temp_range: list) -> None:
    """
    Flashes LED when temperature gets between provided range (list with two int 
    elements), and is solid when within 5 degrees celcius of the limits
    """
    lower, upper = temp_range[0], temp_range[1]
    soft_lower, soft_upper = lower - 5, upper + 5
    outside_range = True

    while outside_range:
        temp = get_temp()
        if lower <= temp <= upper:
            print(f"{temp} C   READY")
            outside_range = send_daily_cat_pic()
            for x in range(50):
                time.sleep(0.25)
                LED_on()
                time.sleep(0.25)
                LED_off()
        elif temp >= soft_lower and temp <= soft_upper:
            LED_on()
            print(f"{temp} C   ALMOST")
            time.sleep(2)
        elif GPIO.input(16) == 1:
            print(temp)
            LED_off()
            time.sleep(2)

def send_daily_cat_pic(): 
    sender_email = "dannypyth@gmail.com"
    password = "ozH{CG)MJarqF2|>m(oQl{(t9ifaf~"
    receiver_email = "danny613tran@gmail.com"
    subject = "Temperature in acceptable range!"
    URL = "https://catoftheday.com/"
    FOLDER_PATH = "/home/pi/Pictures/"

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    images = soup.find_all('img')
    links = []
    for image_tag in images:
        links.append(image_tag['src'])
    image_URL = URL + links[14]
    file_name = str((image_URL.split("/"))[-1])
    file_location = FOLDER_PATH + file_name

    request = requests.get(image_URL, stream=True)
    if request.status_code == 200:  #200 status code = OK
        with open(file_location, 'wb') as f:
            request.raw.decode_content = True
            shutil.copyfileobj(request.raw, f)

    yag = yagmail.SMTP(sender_email, password)
    yag.send(
        to=receiver_email,
        subject=subject,
        contents=yagmail.inline(file_location))
    
    for file_name in os.listdir(FOLDER_PATH):
        file_path = FOLDER_PATH + file_name
        os.remove(file_path)

    return False

# Main script
COFFEE = [60, 70]  # Constant temperature ranges
TEA = [55, 65]
MENU_PROMPT = (
    "1 - Constantly read temperature\n"
    "2 - Optimal temperature for coffee\n"
    "3 - Optimal temperature for tea\n"
    "4 - Set custom temperature ranges\n"
    "CTRL + C to quit any process\n> ")

try: # Allows user to CTRL + C out of the program and properly clean up GPIO pin
    while True:
        user = int(input(MENU_PROMPT))
        if user == 1: 
            command = repeated_get_temp()
        elif user == 2: 
            command = find_temp_range(COFFEE)
        elif user == 3: 
            command = find_temp_range(TEA)
        elif user == 4: 
            command = find_temp_range(
                [
                 float(input("Lower limit\n> ")), 
                 float(input("Upper limit\n> "))
                ]
            )
except:
    LED_off()
    GPIO.cleanup()
