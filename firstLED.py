import RPi.GPIO as GPIO
import time

pins = [16]
pauseTime = 0.5
GPIO.setmode(GPIO.BCM)
GPIO.setup(pins[0],GPIO.OUT)

for x in range(20):
	print("LED on")
	GPIO.output(pins[0],GPIO.HIGH)
	time.sleep(pauseTime)
	print("LED off")
	GPIO.output(pins[0],GPIO.LOW)
	time.sleep(pauseTime)
