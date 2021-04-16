import modules.settings as settings
import pytest

def test_edit_settings_properties():
    sett = settings.Settings()
    # mode
    sett.mode = 'social'
    assert sett.mode == 'social'
    sett.mode = 'non-existent'
    assert sett.mode == 'social'
    # refresh_interval
    sett.mode = 'social'
    sett.refresh_interval = 1
    assert sett.refresh_interval == 1
    sett.refresh_interval = "test"
    assert sett.refresh_interval == 1
    sett.mode = 'weather'
    assert sett.refresh_interval == 30
    # future_forecast_time
    sett.future_forecast_time = 2
    sett.future_forecast_time = "wow"
    assert sett.future_forecast_time == 2
    # brightness
    sett.brightness = 50
    sett.brightness = 101
    sett.brightness = -1
    sett.brightness = "test"
    assert sett.brightness == 50
    # subjects
    sett.subjects = "hoi,kaas,test"
    assert sett.subjects == ['hoi', 'kaas', 'test']
    sett.subjects = ['test1', 'test2']
    assert sett.subjects == ['test1', 'test2']
    sett.subjects = 5
    assert sett.subjects == ['test1', 'test2']
    # location
    sett.location = "1.02,2.01"
    assert sett.location == ['1.02', '2.01']
    sett.location = ['50.1', '100.2']
    assert sett.location == ['50.1', '100.2']
    sett.location = 5
    assert sett.location == ['50.1', '100.2']
    # max_future_forecast_time
    with pytest.raises(AttributeError):
        sett.max_future_forecast_time = 5
        assert sett.max_future_forecast_time == 24

def test_save_load_settings():
    sett = settings.Settings()
    sett.future_forecast_time = 1
    assert sett.future_forecast_time == 1
    sett.future_forecast_time = 2
    sett.save_to_file()
    settings2 = settings.Settings()
    assert settings2.future_forecast_time == 2