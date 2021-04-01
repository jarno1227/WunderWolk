from api import Api
from settings import Settings

class Program:
    def __init__(self, refresh_interval):
        # todo: get latest settings from file or database or something
        self.settings = Settings()
        self.API = Api()
        # self.MQTT = MQTT()
