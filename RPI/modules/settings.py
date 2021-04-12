import json


class Settings:
    # todo: if parameter is empty retrieve data from settingsfile
    def __init__(self):
        # if subjects is None:
        #     # todo: better system to dynamically add the quotations in the fetch commands
        #     subjects = ['"mark rutte"', '"pieter omtzigt"']
        self.available_modes = [
            "weather",
            "social"
        ]
        self._mode = "weather"
        self._refresh_interval = -1
        self._future_forecast_time = -1
        self._brightness = 100
        self._subjects = []
        self._location = [0, 0]
        self.settings_path = "C:\projects\WunderWolk\RPI\modules\data.txt"
        # setup
        # self.save_to_file()
        self.load_from_file()

    def save_settings_json(self, data):
        self.mode = data['mode']
        self.refresh_interval = data['refresh_interval']
        self.future_forecast_time = data['future_forecast_time']
        self.brightness = data['brightness']
        self.subjects = []
        if data['subjects']:
            for subject in data['subjects']:
                self.subjects.append(subject)
        self.location = [data['location']['latitude'], data['location']['longitude']]

    def load_from_file(self):
        with open(self.settings_path) as json_file:
            data = json.load(json_file)
            self.save_settings_json(data)

    def save_to_file(self):
        current_settings = self.to_json()
        # data = {"mode": "weather", "refresh_interval": 5, "future_forecast_time": 30, "brightness": 100,
        #         "subjects": ["test1", "test2"],
        #         "location": {"latitude": 51.57046107093778, "longitude": 5.050113150625251}}

        with open(self.settings_path, "w") as json_file:
            json.dump(current_settings, json_file)

    def to_json(self):
        settings_json = {"mode": self.mode, "refresh_interval": self.refresh_interval,
                         "future_forecast_time": self.future_forecast_time, "brightness": self.brightness,
                         "subjects": self.subjects,
                         "location": {"latitude": self.location[0], "longitude": self.location[1]}}
        return settings_json

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        if value in self.available_modes:
            self._mode = value
        else:
            print("mode does not exist")

    @property
    def refresh_interval(self):
        return self._refresh_interval

    @refresh_interval.setter
    def refresh_interval(self, value):
        try:
            value = int(value)
            self._refresh_interval = value
        except ValueError:
            value + " is not a correct integer"

    @property
    def future_forecast_time(self):
        return self._future_forecast_time

    @future_forecast_time.setter
    def future_forecast_time(self, value):
        try:
            value = int(value)
            if value <= 48:  # 48 is the max hours in the future from 8am in the morning you can request
                self._future_forecast_time = value
        except ValueError:
            value + " is not a correct integer"

    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    def brightness(self, value):
        try:
            value = int(value)
            if 0 <= value <= 100:
                self._brightness = value
        except ValueError:
            value + " is not a correct integer"

    @property
    def subjects(self):
        return self._subjects

    @subjects.setter
    def subjects(self, value):
        # strings with formatting "value1,value2,...,value5"
        if type(value) is str:
            value = value.split(",")
        self._subjects = value

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        # strings with formatting "longitude,latitude"
        if type(value) is str:
            value = value.split(",")
        self._location = value
