import schedule
import pigpio
import threading
from time import sleep


def arduino_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def thunder_effect_threaded(hardware):
    job_thread = threading.Thread(target=hardware.thunder_effect)
    job_thread.start()


class Hardware:
    def __init__(self):
        self.pins = {
            'pump': 13,
            'stripR': 21,
            'stripG': 20,
            'stripB': 16,
        }
        self.previous_thunder_ledstate = 0
        self.gpio = pigpio.pi()
        self.reset()

    def reset(self):
        schedule.clear('thunder_task')
        self.set_ledstrip((0, 0, 0))
        self.set_pump(0)

    def set_pump(self, speed=0):
        self.gpio.set_PWM_dutycycle(self.pins['pump'], speed)

    def set_ledstrip(self, rgb):
        self.gpio.set_PWM_dutycycle(self.pins['stripR'], rgb[0])
        self.gpio.set_PWM_dutycycle(self.pins['stripG'], rgb[1])
        self.gpio.set_PWM_dutycycle(self.pins['stripB'], rgb[2])

    def thunder_leds(self):
        self.set_ledstrip((42, 4, 84))  # dark purple
        schedule.every(1).to(7).seconds.do(thunder_effect_threaded, self).tag('thunder_task')

    def thunder_effect(self):
        self.set_ledstrip((255, 175, 175))  # white for thunder
        sleep(0.3)
        self.set_ledstrip((42, 4, 84))  # dark purple
        sleep(0.3)
        self.set_ledstrip((255, 175, 175))  # white for thunder
        sleep(0.6)
        self.set_ledstrip((42, 4, 84))  # dark purple

    def make_thunder(self):
        self.reset()
        self.set_pump(200)
        self.thunder_leds()

    def make_sunny(self, value, min=0, max=255):
        self.reset()
        brightness = arduino_map(value, 0, 100, min, max)
        self.set_ledstrip((brightness, 50, 50))

    def set_all(self, rgb, speed):
        self.reset()
        self.set_pump(speed)
        self.set_ledstrip(rgb)
