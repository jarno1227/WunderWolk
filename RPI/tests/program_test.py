import modules.program as program
import modules.settings as settings
import time

prog = program.Program(settings.Settings())


def test_arduino_map():
    val = 1023
    assert program.arduino_map(val, 0, 1023, 0, 255) == 255


def test_change_interval_task():
    assert program.change_interval_task('test', 20) == 20
    program.cancel_task('test')


def test_program_mqtt():
    prog.MQTT.subscribe_topic("pacotinie@gmail.com/app")
    prog.MQTT.send_message("test")
    time.sleep(1)  # sleep because sending the message takes time
    assert prog.MQTT.messages[0] == "test"




def test_get_social_rating():
    prog = program.Program(settings.Settings())
    prog.settings.subjects = ['max verstappen']
    assert len(prog.get_current_social_rating()) > 0
# def test_create_program():
#     program = prog.Program()
