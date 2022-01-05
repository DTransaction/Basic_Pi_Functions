import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)

for x in range(20):
	print("LED on")
	GPIO.output(18,GPIO.HIGH)
	time.sleep(0.03)
	print("LED off")
	GPIO.output(18,GPIO.LOW)
	time.sleep(0.03)
