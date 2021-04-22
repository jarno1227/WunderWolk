import requests
from abc import ABC, abstractmethod
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
        super(SocialConnect, self).__init__(key, settings, 'https://api.social-searcher.com/v2/')

    def calc_avg_sentiment(self, posts_obj):
        negatives, positives, neutrals = 0, 0, 0
        for post in posts_obj['posts']:
            if post['sentiment'] == "negative":
                negatives += 1
            elif post['sentiment'] == "positive":
                positives += 1
            elif post['sentiment'] == "neutral":
                neutrals += 1
        total = negatives + positives  # + neutrals
        negatives_percentage = negatives / total * 100
        positives_percentage = positives / total * 100
        # neutrals_percentage = neutrals / total * 100
        rating = [positives_percentage, negatives_percentage]
        return rating

    def fetch_data(self):
        search_type = 'search'
        subject_counter = 0
        subject_count = len(self.settings.subjects)
        query = ''
        for subject in self.settings.subjects:
            query += f'"{subject}"'
            if subject_counter < subject_count:
                query += 'OR'
            subject_counter += 1
        payload = {'q': query, 'network': 'reddit,twitter,facebook', 'limit': 20, 'key': self.api_key,
                   'lang': 'nl'}  # 'fields': 'sentiment,network,type,lang',
        url = self.base_url + search_type
        # request data from api using the base url and the parameter payload.
        r = requests.get(url, params=payload).text
        # serialize plaintext response to json
        posts_obj = json.loads(r)
        return posts_obj


class WeatherConnect(Api):
    def __init__(self, key, settings):
        super(WeatherConnect, self).__init__(key, settings, 'https://api.openweathermap.org/data/2.5/')
        location = self.settings.location
        self.coordinates = "lat=" + str(location[0]) + "&lon=" + str(location[1])
        self.exclusions = "exclude=" + "current,minutely,daily"
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

    def fetch_hourly_2_days(self):
        r = requests.get(self._complete_url)
        content_string = r.text
        content_obj = json.loads(content_string)
        return content_obj['hourly']

    def fetch_data(self):
        pass
