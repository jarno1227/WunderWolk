from modules.api import SocialConnect, WeatherConnect
from modules.settings import Settings

class Program:
    def __init__(self):
        # todo: get latest settings from file or database or something
        self.settings = Settings(location=[51.57046107093778, 5.050113150625251])
        # self.API = Api()
        self.SocialConnect = SocialConnect("aapje", settings=self.settings)
        self.WeatherConnect = WeatherConnect("f71af11b8e02b30c2ed988487f0dd533", settings=self.settings)
        self.WeatherConnect.fetch_data()
        # self.MQTT = MQTT()
