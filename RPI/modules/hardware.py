import schedule

has_pigpio = False
try:
    import pigpio

    has_pigpio = True
except:
    print("gpio not initialized")
import threading
from time import sleep


def arduino_map(x, in_min, in_max, out_min, out_max):
    if x > in_max:
        x = in_max
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def thunder_effect_threaded(hardware):
    job_thread = threading.Thread(target=hardware.thunder_effect)
    job_thread.start()


class Hardware:
    def __init__(self, settings):
        self.pins = {
            'pump': 13,
            'stripR': 21,
            'stripG': 20,
            'stripB': 16,
        }
        self.pinValues = {
            'pump': 0,
            'stripR': 0,
            'stripG': 0,
            'stripB': 0,
        }
        self.settings = settings
        if has_pigpio:
            self.gpio = pigpio.pi()
        self.reset()

    def reset(self):
        schedule.clear('thunder_task')
        self.set_ledstrip((0, 0, 0))
        self.set_pump(0)

    def set_pump(self, speed=0):
        if has_pigpio:
            self.gpio.set_PWM_dutycycle(self.pins['pump'], speed)

    def set_ledstrip(self, rgb):
        if has_pigpio:
            self.pinValues['stripR'] = rgb[0]
            self.pinValues['stripG'] = rgb[1]
            self.pinValues['stripB'] = rgb[2]
            r = int(self.pinValues['stripR'] / 100 * self.settings.brightness)
            g = int(self.pinValues['stripG'] / 100 * self.settings.brightness)
            b = int(self.pinValues['stripB'] / 100 * self.settings.brightness)
            self.gpio.set_PWM_dutycycle(self.pins['stripR'], r)
            self.gpio.set_PWM_dutycycle(self.pins['stripG'], g)
            self.gpio.set_PWM_dutycycle(self.pins['stripB'], b)

    def update_brightness(self):
        self.set_ledstrip((self.pinValues['stripR'], self.pinValues['stripG'], self.pinValues['stripB']))

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

    def make_sunny(self, value, min_input=0, max_input=100, min_output=0, max_output=60):
        self.reset()
        brightness = arduino_map(value, min_input, max_input, min_output, max_output)
        self.set_ledstrip((255, brightness, 0))

    def set_all(self, rgb, speed):
        self.reset()
        self.set_pump(speed)
        self.set_ledstrip(rgb)
