from modules.api import SocialConnect, WeatherConnect
from modules.settings import Settings
from modules.mqtt import MQTT
import time
import schedule



class Program:
    def __init__(self):
        # todo: get latest settings from file or database or something
        self.settings = Settings()
        self.hourly_weather = None
        self.SocialConnect = SocialConnect("bddae9b9df86095e0d4b9908a7a9b622", settings=self.settings)
        self.WeatherConnect = WeatherConnect("f71af11b8e02b30c2ed988487f0dd533", settings=self.settings)
        self.get_current_social_rating()
        self.MQTT = MQTT("pacotinie@gmail.com", "Bepperking!")
        self.MQTT.subscribe_topic("pacotinie@gmail.com/settings")
        self.refresh_config()

        while True:
            schedule.run_pending()
            time.sleep(0.1)

    def get_current_social_rating(self):
        posts_obj = self.SocialConnect.fetch_data()
        rating = self.SocialConnect.calc_avg_sentiment(posts_obj)
        print(rating)
    
    def refresh_config(self):
        # settings
        self.hourly_weather = self.WeatherConnect.fetch_hourly_2_days()
        schedule.every(0.1).seconds.do(self.check_messages)

    def check_messages(self):
        if len(self.MQTT.messages) > 0:
            msg = self.MQTT.retrieve_message()
            print(msg)

    def process_messages(self):
        pass
