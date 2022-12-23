from picamera import PiCamera
import time

camera = PiCamera()

camera.start_preview()
time.sleep(5)
camera.capture('/home/dannypizero/PROOF/' + time.ctime())
camera.stop_preview()