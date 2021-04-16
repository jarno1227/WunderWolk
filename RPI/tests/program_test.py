import modules.program as prog


def test_arduino_map():
    val = 1023
    assert prog.arduino_map(val, 0, 1023, 0, 255) == 255


def test_change_interval_task():
    assert prog.change_interval_task('test', 20) == 20
    prog.cancel_task('test')




# def test_create_program():
#     program = prog.Program()
