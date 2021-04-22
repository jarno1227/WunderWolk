import modules.program as program
import modules.settings as settings
import modules.api as api_conn

socialkey = "bddae9b9df86095e0d4b9908a7a9b622"
weatherkey = "f71af11b8e02b30c2ed988487f0dd533"
settings = settings.Settings()
weather_connect = api_conn.WeatherConnect(weatherkey, settings)
social_connect = api_conn.SocialConnect(socialkey, settings)


def test_fetch_weather_hourly_2_days():
    forecast_time = weather_connect.fetch_hourly_2_days()
    assert isinstance(forecast_time, object)
    assert len(forecast_time) > 0

def test_weather_update_url():
    weather_connect.coordinates = "lat=" + str(1) + "&lon=" + str(5)
    weather_connect.exclusions = "exclude=current"
    weather_connect.units = "units=imperial"
    weather_connect.app_id = "appid=test_id"
    weather_connect.update_url()
    assert weather_connect.complete_url == "https://api.openweathermap.org/data/2.5/onecall?" + \
           weather_connect.coordinates + "&exclude=current&units=imperial&appid=test_id"
    weather_connect.complete_url = "wow wat gaaf"
    assert weather_connect.complete_url == "wow wat gaaf"

def test_fetch_social_data_calc_avg():
    social_data = social_connect.fetch_data()
    assert isinstance(social_data, object)
    assert len(social_data) > 0
    rating = social_connect.calc_avg_sentiment(social_data)
    assert type(rating) is list
    assert len(rating) > 0

def test_API_properties():
    weather_connect.api_key = "test"
    assert weather_connect.api_key == "test"
    weather_connect.settings = "settings as string"
    assert weather_connect.settings == "settings as string"
    weather_connect.base_url = "newbaseurl"
    assert weather_connect.base_url == "newbaseurl"

