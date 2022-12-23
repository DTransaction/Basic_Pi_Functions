from picamera import PiCamera
import time

camera = PiCamera()

location = "/home/dannypi/" + time.ctime(time.time()) + ".jpg"
camera.capture(location)