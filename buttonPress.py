import time
import RPi.GPIO as GPIO

#General Setup
pins = [18]
GPIO.setmode(GPIO.BCM) #sets how we reference GPIO pins
GPIO.setup(pins, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #set GPIO pins

print("Begin") #informs user the main function of the program is begi

try:
	while True:
		if GPIO.input(pins[0]) == GPIO.HIGH:
			print("nice")
			time.sleep(0.3)
except:
	GPIO.cleanup() #cleansup all of the GPIO pins used within the script
	print("Done") #informs the user the program is finished running
