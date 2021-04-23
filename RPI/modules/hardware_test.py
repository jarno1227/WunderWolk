from modules.hardware import *
from modules.settings import Settings
import time
import schedule
from random import randint

# testfile is in modules as it is not a unit test but a hardware test
s = Settings
h = Hardware(s)


def start_scheduler():
    try:
        while True:
            schedule.run_pending()
            time.sleep(0.1)
    except KeyboardInterrupt:
        h.reset()


def test_arduino_map():
    val = 1023
    assert arduino_map(val, 0, 1023, 0, 255) == 255


def test_thunder_effect_threaded():
    thunder_effect_threaded(h)


def test_reset():
    h.reset()


def test_set_pump():
    h.set_pump(speed=100)


def test_set_ledstrip():
    rgb = (100, 100, 100)
    h.set_ledstrip(rgb)


def test_update_brightness():
    h.update_brightness()


def test_thunder_leds():
    h.thunder_leds()
    start_scheduler()


def test_thunder_effect():
    h.thunder_effect()


def test_make_thunder():
    h.make_thunder()
    start_scheduler()


def test_make_sunny():
    h.make_sunny(value=randint(60, 100))


def test_set_all():
    r = randint(0, 255)
    g = randint(0, 175)
    b = randint(0, 175)
    speed = randint(50, 255)
    h.set_all((r, g, b), speed)
