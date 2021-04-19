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


def test_get_social_rating():
    prog.settings.subjects = ['max verstappen']
    assert len(prog.get_current_social_rating()) > 0


def test_program_mqtt():
    prog.MQTT.subscribe_topic("pacotinie@gmail.com/app")
    prog.MQTT.send_message("test")
    time.sleep(1)  # sleep because sending the message takes time
    assert prog.MQTT.messages[0] == "test"
    prog.MQTT.retrieve_message()


def test_check_messages_program():
    msg = prog.check_messages()
    assert msg == None
    prog.MQTT.messages.append("testvalue")
    msg = prog.check_messages()
    assert msg == "testvalue"


def test_process_messages():
    prog.MQTT.subscribe_topic("pacotinie@gmail.com/app")
    prog.settings.mode = 'weather'
    prog.settings.brightness = '50'
    # request
    prog.process_messages("request|settings")
    time.sleep(1)
    msg = prog.MQTT.retrieve_message()
    #     todo: check if msg  json string
    prog.process_messages("request|mode")
    time.sleep(1)
    msg = prog.MQTT.retrieve_message()
    assert msg == 'weather'
    # settings
    prog.process_messages("settings|{'mode': 'social', 'refresh_interval': 5, 'future_forecast_time': 1, 'brightness': 50, 'subjects': ['max verstappen'], 'location': {'latitude': 51.57046107093778, 'longitude': 5.050113150625251}}")
    assert prog.settings.mode == 'social'
    # save specific
    assert prog.settings.brightness == 50
    prog.process_messages("brightness|70")
    assert prog.settings.brightness == 70
    # todo: msg_type mode or refresh_interval, check if change interval is changed


def test_handle_weather():
    assert prog.handle_weather() is not False
    # todo: think how i display succes with weather handling
