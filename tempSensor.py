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
pins = [16, 27] # Initializes the GPIO pin of the LED
GPIO.setmode(GPIO.BCM)
GPIO.setup(pins[0], GPIO.OUT)
GPIO.setup(pins[1], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setwarnings(False)

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_path = glob.glob(base_dir + '28*')[0] # Gets the file path of sensor



# Function definitions
def LED_on(): GPIO.output(pins[0], GPIO.HIGH)

def LED_off(): GPIO.output(pins[0], GPIO.LOW)

def LED_flash(times: int):
    for x in range(times):
        LED_on()
        time.sleep(0.25)
        LED_off()
        time.sleep(0.25)

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

    return True

def find_temp_range(temp_range: list) -> None:
    """
    Flashes LED when temperature gets between provided range (list with two int 
    elements), and is solid when within 5 degrees celcius of the limits
    """
    lower, upper = temp_range[0], temp_range[1]
    soft_lower, soft_upper = lower - 5, upper + 5
    inside_range = False

    while not inside_range:
        temp = get_temp()
        if lower <= temp <= upper:
            print(f"{temp} C   READY")
            inside_range = send_daily_cat_pic()
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



# Main script
COFFEE = [60, 70]  # Constant temperature ranges
TEA = [55, 65]

counter = 0
complete = False
began = False


print("Begin")

while not complete: 
    while GPIO.input(pins[1]) == GPIO.HIGH:
        LED_flash(1)
        counter += 1
        began = True
        print(counter)
    start_time = time.time()
    replay = True
    while GPIO.input(pins[1]) == GPIO.LOW and began:
        end_time = time.time()
        time_elapsed = end_time - start_time
        if time_elapsed >= 10:
            print("Setting range in 30 seconds")
            # time.sleep(30)
            find_temp_range([counter * 10 - 3, counter * 10 + 3])
            complete = True
            break
        elif time_elapsed >= 3 and replay:
            print("Replaying")
            LED_flash(counter)
            replay = False

GPIO.cleanup() #cleansup all of the GPIO pins used within the script
print("Done") #informs the user the program is finished running