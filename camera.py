from picamera import PiCamera
import time

camera = PiCamera()

location = "/home/dannypi/" + time.ctime(time.time() - 18000) + ".jpg"
camera.capture(location)