import requests
from abc import ABC, abstractmethod


class Api(ABC):
    def __init__(self, key):
        self._api_key = key

    @property
    def api_key(self):
        return self._api_key

    @api_key.setter
    def api_key(self, val):
        self._api_key = val

    @abstractmethod
    def fetch_data(self):
        pass


class SocialConnect(Api):
    def __init__(self, key, settings):
        super().__init__(key)

    def fetch_data(self):
        pass


class WeatherConnect(Api):
    def __init__(self, key, settings):
        super(WeatherConnect, self).__init__(key)
        self.baseUrl = "https://api.openweathermap.org/data/2.5/onecall?"
        self.coordinates = "lat=" + str(settings.location[0]) + "&lon=" + str(settings.location[1])
        self.exclusions = "exclude=" + "current,minutely,daily"
        self.units = "units=" + "metric"
        self.app_id = "appid=" + self.api_key
        self._complete_url = ""
        self.update_url()

    def update_url(self):
        self._complete_url = self.baseUrl + self.coordinates + "&" + self.exclusions + "&" \
                             + self.units + "&" + self.app_id

    @property
    def complete_url(self):
        return self._complete_url

    @complete_url.setter
    def complete_url(self, value):
        self._complete_url = value

    def fetch_data(self):
        r = requests.get(self._complete_url)
        print(r.content)
