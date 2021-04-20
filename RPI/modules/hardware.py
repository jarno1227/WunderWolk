def arduino_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


class Hardware:
    def __init__(self, pins, states):
        self.pins = {
            'pump': 0,
            'stripR': 0,
            'stripG': 0,
            'stripB': 0,
        }

    def set_pump(self, speed):
        pass

    def set_ledstrip(self, rgb):
        pass
