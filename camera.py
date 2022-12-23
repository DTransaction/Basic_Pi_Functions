from picamera import PiCamera
import time

camera = PiCamera()

location = "/home/dannypi/" + time.localtime + ".jpg"
print(location)
camera.capture(location)