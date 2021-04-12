from modules.api import SocialConnect, WeatherConnect
from modules.settings import Settings
from modules.mqtt import MQTT
import time
import schedule
import json


def run_program():
    program_settings = Settings()
    program = Program(program_settings)
    schedule.every(0.1).seconds.do(program.check_messages)
    while True:
        schedule.run_pending()
        time.sleep(0.1)


class Program:
    def __init__(self, settings):
        self.settings = settings
        self.hourly_weather = None
        self.SocialConnect = SocialConnect("bddae9b9df86095e0d4b9908a7a9b622", settings=self.settings)
        self.WeatherConnect = WeatherConnect("f71af11b8e02b30c2ed988487f0dd533", settings=self.settings)
        # self.get_current_social_rating()
        self.MQTT = MQTT("pacotinie@gmail.com", "Bepperking!")
        self.MQTT.subscribe_topic("pacotinie@gmail.com/rpi")
        # self.hourly_weather = self.WeatherConnect.fetch_hourly_2_days()

    def get_current_social_rating(self):
        posts_obj = self.SocialConnect.fetch_data()
        rating = self.SocialConnect.calc_avg_sentiment(posts_obj)

    def get_coming_weather(self):
        self.WeatherConnect.fetch_hourly_2_days()

    def check_messages(self):
        if len(self.MQTT.messages) > 0:
            msg = self.MQTT.retrieve_message()
            self.process_messages(msg)

    def process_messages(self, msg):
        # mqtt message is constructed as -> type|value
        delimiter = "|"
        msg_split = msg.split(delimiter)
        if len(msg_split) > 1:
            msg_type = msg_split[0]
            value = msg_split[1]
            if msg_type == "request":
                if value == "settings":
                    self.MQTT.send_message("pacotinie@gmail.com/app", str(self.settings.to_json()))
                elif hasattr(self.settings, value):
                    self.MQTT.send_message("pacotinie@gmail.com/app", json.dumps(getattr(self.settings, value)))

            elif msg_type == "settings":  # save all settings at once
                value = value.replace("'", '"')  # single quotes to double for json parser
                self.settings.save_settings_json(json.loads(value))
            else:  # save specific setting
                if hasattr(self.settings, msg_type):
                    setattr(self.settings, msg_type, value)
