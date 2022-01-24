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

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_path = glob.glob(base_dir + '28*')[0] # Gets the file path of sensor



# Function definitions
def LED_on(): GPIO.output(pins[0], GPIO.HIGH)

def LED_off(): GPIO.output(pins[0], GPIO.LOW)

def LED_flash(times: int, pause: float) -> None:
    for x in range(times):
        LED_on()
        time.sleep(pause)
        LED_off()
        time.sleep(pause)

def get_temp() -> float:
    with open(device_path + '/w1_slave', 'r') as f:
        temp = int((str(f.readlines()))[76:81])/1000
    return temp

def email_daily_cat_pic(data: list) -> None: 
    sender_email = "dannypyth@gmail.com"
    password = "ozH{CG)MJarqF2|>m(oQl{(t9ifaf~"
    receiver_email = "mt1337@gmail.com"
    subject = f"Sensor is now {data[2]}\xb0C, within ({data[0]}\xb0C, {data[1]}\xb0C)"
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
        if lower <= temp and temp <= upper:
            print(f"{temp} C   READY")
            email_daily_cat_pic(temp_range + [temp])
            LED_flash(50, 0.25)
            inside_range = True
        elif temp >= soft_lower and temp <= soft_upper:
            print(f"{temp} C   ALMOST")
            LED_on()
            time.sleep(2)
        else:
            print(temp)
            LED_off()
            time.sleep(2)



# Main script
print("Begin")
while True: 
    try:
        began = False
        counter = 0
        while GPIO.input(pins[1]) == GPIO.HIGH:
            began = True
            counter += 1
            print(counter)
            LED_flash(1, 0.3)
        start_time = time.time()
        replay = True
        while GPIO.input(pins[1]) == GPIO.LOW and began:
            end_time = time.time()
            time_elapsed = end_time - start_time
            if time_elapsed >= 10:
                lower_limit = counter * 10 - 3
                upper_limit = counter * 10 - 3
                print(f"Range is set to ({lower_limit}\xb0C, {upper_limit}\xb0C)\n"
                       "Starting in 30 seconds\n"
                       "Place temperature sensor in the stuff\n")
                # time.sleep(30)
                find_temp_range([lower_limit, upper_limit])
                break
            elif time_elapsed >= 3 and replay:
                print("Replaying")
                LED_flash(counter, 0.2)
                replay = False
    except Exception as e:
        print(f"{e}\nDone")
        LED_off
        GPIO.cleanup()
        break