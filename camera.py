from picamera2 import PiCamera
import time

camera = PiCamera()

camera.resolution = (2592, 1944)
camera.capture('/home/dannypizero/PROOF/' + time.ctime())
