from modules.api import SocialConnect, WeatherConnect
from modules.settings import Settings
from modules.mqtt import MQTT
import time
import datetime
import pytz
import schedule
import json


def arduino_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def change_interval_task(task_tag, interval=60):
    schedule.clear(task_tag)
    schedule.every(interval).minutes.do(refresh_api).tag(task_tag)


def refresh_api(program):
    if program.settings.mode == "weather":
        program.handle_weather()
    elif program.settings.mode == "social":
        print("im very social")
        # rating = program.get_current_social_rating()


def run_program():
    program = Program(Settings())
    # print(vars(program.settings))
    schedule.every(0.1).seconds.do(program.check_messages).tag('read-mqtt')
    program.settings.mode = 'weather'
    program.settings.future_forecast_time = 1
    schedule.every(program.settings.refresh_interval).minutes.do(refresh_api, program).tag('api-handling')
    program.handle_weather()

    while True:
        schedule.run_pending()
        time.sleep(0.1)


def weather_parse(code):
    if 300 > code >= 200:  # thunderstorm
        pass
    elif 400 > code >= 300:  # drizzle
        pass
    elif 600 > code >= 500:  # rain
        pass
    elif 700 > code > 600:  # snow
        pass
    elif 800 > code >= 700:  # atmosphere
        pass
    elif code == 800:  # clear sky
        pass
    elif 900 > code > 800:  # clouds
        pass


class Program:
    def __init__(self, settings):
        self.settings = settings
        self.SocialConnect = SocialConnect("bddae9b9df86095e0d4b9908a7a9b622", settings=self.settings)
        self.WeatherConnect = WeatherConnect("f71af11b8e02b30c2ed988487f0dd533", settings=self.settings)
        self.MQTT = MQTT("pacotinie@gmail.com", "Bepperking!")
        self.MQTT.subscribe_topic("pacotinie@gmail.com/rpi")
        self.hourly_weather = []

    def get_current_social_rating(self):
        posts_obj = self.SocialConnect.fetch_data()
        return self.SocialConnect.calc_avg_sentiment(posts_obj)

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
                    self.MQTT.send_message(str(self.settings.to_json()))
                elif hasattr(self.settings, value):
                    self.MQTT.send_message(json.dumps(getattr(self.settings, value)))

            elif msg_type == "settings":  # save all settings at once #todo: check json parsing
                value = value.replace("'", '"')  # single quotes to double for json parser
                try:
                    self.settings.save_settings_json(json.loads(value))
                    self.settings.save_to_file()
                except ValueError as e:
                    self.MQTT.send_message("not a correct json")

            else:  # save specific setting
                if hasattr(self.settings, msg_type):
                    setattr(self.settings, msg_type, value)
                    self.settings.save_to_file()
                    if msg_type == "mode" or msg_type == "refresh_interval":
                        change_interval_task('api-handling', self.settings.refresh_interval)
            print("new settings" + str(vars(self.settings)))

    def handle_weather(self):
        self.hourly_weather = self.WeatherConnect.fetch_hourly_2_days()

        if self.settings.future_forecast_time <= self.settings.max_future_forecast_time:
            timezone = pytz.timezone('Europe/Amsterdam')
            now_with_future_forecast_time = datetime.datetime.now(timezone) + datetime.timedelta(
                hours=self.settings.future_forecast_time)
            if now_with_future_forecast_time.minute > 30:
                now_with_future_forecast_time += datetime.timedelta(hours=1)
            for hour_of_estimation in self.hourly_weather:
                hour_of_estimation_timezoned = datetime.datetime.fromtimestamp(hour_of_estimation['dt'], timezone)
                weather_code = hour_of_estimation['weather'][0]['id']
                print(weather_code)
                # if hour_of_estimation_timezoned > now_with_future_forecast_time:
                #     print(hour_of_estimation)
                #     print(hour_of_estimation_timezoned)
                #     return True
            return False
