import requests
from abc import ABC, abstractmethod
import datetime
import json


class Api(ABC):
    def __init__(self, key, settings, base_url):
        self._api_key = key
        self._settings = settings
        self._base_url = base_url

    @property
    def api_key(self):
        return self._api_key

    @api_key.setter
    def api_key(self, val):
        self._api_key = val

    @property
    def settings(self):
        return self._settings

    @settings.setter
    def settings(self, value):
        self._settings = value

    @property
    def base_url(self):
        return self._base_url

    @base_url.setter
    def base_url(self, value):
        self._base_url = value

    @abstractmethod
    def fetch_data(self):
        pass


class SocialConnect(Api):
    def __init__(self, key, settings):
        super().__init__(key, settings, "https://api.social-searcher.com/v2/")

    def fetch_data(self):
        search_type = "search?"
        subject_counter = 0
        subject_count = len(self.settings.subjects)
        query = ''
        for subject in self.settings.subjects:
            # fixme: termen met spatie krijgen een + ipv spatie. Volgens doc moet je er dubbele haakjes om heen zetten
            query += '"' + subject + '"'
            if subject_counter < subject_count:
                query += 'OR'
            subject_counter += 1
        payload = {'key': self.api_key, 'q': query, 'network': 'web'}
        url = self.base_url + search_type
        r = requests.get(url, params=payload)
        print(r.url)
        content_string = r.text
        content_obj = json.loads(content_string)
        for post in content_obj['posts']:
            print(post['sentiment'])


class WeatherConnect(Api):
    def __init__(self, key, settings):
        super(WeatherConnect, self).__init__(key, settings, "https://api.openweathermap.org/data/2.5/")
        self.coordinates = "lat=" + str(settings.location[0]) + "&lon=" + str(settings.location[1])
        self.exclusions = "exclude=" + "current,minutely,daily"  # + ",hourly"
        self.units = "units=" + "metric"
        self.app_id = "appid=" + self.api_key
        self._complete_url = ""
        self.update_url()

    def update_url(self):
        self._complete_url = self.base_url + "onecall?" + self.coordinates + "&" + self.exclusions + "&" \
                             + self.units + "&" + self.app_id

    @property
    def complete_url(self):
        return self._complete_url

    @complete_url.setter
    def complete_url(self, value):
        self._complete_url = value

    def fetch_hourly(self):
        r = requests.get(self._complete_url)
        content_string = r.text
        content_obj = json.loads(content_string)
        for hour in content_obj['hourly']:
            print(datetime.datetime.utcfromtimestamp(hour['dt']))

        return content_obj

    def fetch_data(self):
        pass
