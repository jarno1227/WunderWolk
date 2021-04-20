from modules.hardware import *

# h = Hardware()


def test_arduino_map():
    val = 1023
    assert arduino_map(val, 0, 1023, 0, 255) == 255
