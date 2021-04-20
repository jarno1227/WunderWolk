import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)

while True:
    GPIO.output(4, 1)
    sleep(1)
    GPIO.output(4, 0)
    sleep(1)