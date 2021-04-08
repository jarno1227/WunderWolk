class Settings:
    available_modes = [
        "weather",
        "social"
    ]

    # todo: if parameter is empty retrieve data from settingsfile
    def __init__(self, mode="weather", refresh_interval=5, future_forecast_time=30, brightness=100, subjects=None, location="woerden"):
        if subjects is None:
            # todo: better system to dynamically add the quotations in the fetch commands
            subjects = ['"mark rutte"', '"pieter omtzigt"']
        self.mode = mode
        self.refresh_interval = refresh_interval
        self.future_forecast_time = future_forecast_time
        self.brightness = brightness
        self.subjects = subjects
        self.location = location

