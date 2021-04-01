class Settings:
    available_modes = [
        "weather",
        "social"
    ]

    # todo: if parameter is empty retrieve data from settingsfile
    def __init__(self, mode="weather", refresh_interval=5, future_forecast_time=30, brightness=100, subjects=[]):
        self.mode = mode
        self.refresh_interval = refresh_interval
        self.future_forecast_time = future_forecast_time
        self.brightness = brightness
        self.subjects = subjects
