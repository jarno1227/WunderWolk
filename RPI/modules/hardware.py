import schedule


def arduino_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


class Hardware:
    def __init__(self):
        self.pins = {
            'pump': 0,
            'stripR': 0,
            'stripG': 0,
            'stripB': 0,
        }

    def reset(self):
        #todo cancel scheduled tasks
        self.set_ledstrip((0, 0, 0), 0)
        self.set_pump()

    def set_pump(self, speed=0):
        pass

    def set_ledstrip(self, rgb, brightness):
        pass

    def thunder_leds(self):
        pass
        # cool effects thunder with scheduling

    def make_thunder(self):
        self.reset()
        self.set_pump(255)
        self.thunder_leds()

    def make_sunny(self, value, min=0, max=255):
        self.reset()
        brightness = arduino_map(value, 0, 100, min, max)
        self.set_ledstrip((255, 255, 102), brightness)

