import time
import RPi.GPIO as GPIO

#General Setup
pins = [27, 16]
GPIO.setmode(GPIO.BCM)  # Sets how we reference GPIO pins
GPIO.setup(pins[0], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  
GPIO.setup(pins[1], GPIO.OUT)
GPIO.setwarnings(False)
print("Begin")


def LED_flash(times: int):
    for x in range(times):
        GPIO.output(pins[1], GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(pins[1], GPIO.LOW)
        time.sleep(0.2)

counter = 0
complete = False

while not complete: 
    while GPIO.input(pins[0]) == GPIO.HIGH:
        LED_flash(1)
        counter += 1
    start_time = time.time()
    if GPIO.input(pins[0]) == GPIO.LOW:
        end_time = time.time()
        time_elapsed = end_time - start_time
        if time_elapsed >= 5:
            LED_flash(counter)
            complete = True
            

GPIO.cleanup() #cleansup all of the GPIO pins used within the script
print("Done") #informs the user the program is finished running