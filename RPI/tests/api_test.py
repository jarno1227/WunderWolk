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


def test_fetch_social_data_calc_avg():
    social_data = social_connect.fetch_data()
    assert isinstance(social_data, object)
    assert len(social_data) > 0
    rating = social_connect.calc_avg_sentiment(social_data)
    assert type(rating) is list
    assert len(rating) > 0

