import schedule
import pigpio
import threading
from time import sleep


def arduino_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def thunder_storm_threaded(hardware):
    print("wow")
    job_thread = threading.Thread(target=hardware.thunder_effect)
    job_thread.start()


class Hardware:
    def __init__(self):
        self.pins = {
            'pump': 0,
            'stripR': 21,
            'stripG': 20,
            'stripB': 16,
        }
        self.previous_thunder_ledstate = 0
        self.gpio = pigpio.pi()
        self.reset()

    def reset(self):
        schedule.clear()
        self.set_ledstrip((0, 0, 0))
        self.set_pump(0)

    def set_pump(self, speed=0):
        pass
        # self.gpio.set_PWM_dutycycle(self.pins['pump'], speed)

    def set_ledstrip(self, rgb):
        self.gpio.set_PWM_dutycycle(self.pins['stripR'], rgb[0])
        self.gpio.set_PWM_dutycycle(self.pins['stripG'], rgb[1])
        self.gpio.set_PWM_dutycycle(self.pins['stripB'], rgb[2])

    def thunder_leds(self):
        self.set_ledstrip((42, 4, 84))  # dark purple
        schedule.every(1).to(7).seconds.do(thunder_storm_threaded, self).tag('thunder_task')

    def thunder_effect(self):
        self.set_ledstrip((255, 255, 255))  # white for thunder
        sleep(1)
        self.set_ledstrip((42, 4, 84))  # dark purple

    def make_thunder(self):
        self.reset()
        self.set_pump(255)
        self.thunder_leds()

    def make_sunny(self, value, min=0, max=255):
        self.reset()
        brightness = arduino_map(value, 0, 100, min, max)
        self.set_ledstrip((brightness, 255, 255))
