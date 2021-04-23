from modules.api import SocialConnect, WeatherConnect
from modules.settings import Settings
from modules.mqtt import MQTT
import time
import datetime
import pytz
import schedule
import json
from random import randint

from modules.hardware import Hardware

sett = Settings()
h = Hardware(sett)


def change_interval_task(task_tag, interval=60, program=None):
    if program is None:
        return print("Task scheduling has not been changed")
    schedule.clear(task_tag)
    schedule.every(interval).seconds.do(program.refresh_api).tag(task_tag)
    return interval


def check_and_parse_message(program):
    msg = program.check_messages()
    if msg is not None:
        program.process_messages(msg)


def cancel_task(task_tag):
    schedule.clear(task_tag)


def run_program():
    program = Program(sett)
    schedule.every(0.1).seconds.do(check_and_parse_message, program).tag('read-mqtt')
    schedule.every(program.settings.refresh_interval).seconds.do(program.refresh_api).tag('api-handling')
    print("program started")
    print("current settings" + str(vars(program.settings)))

    while True:
        schedule.run_pending()
        time.sleep(0.1)


def weather_parse(hour_data):
    weather_code = hour_data['weather'][0]['id']
    try:
        if 300 > weather_code >= 200:  # thunderstorm
            h.make_thunder()
        elif 400 > weather_code >= 300:  # drizzle
            h.set_all((102, 204, 255), 50)
        elif 600 > weather_code >= 500:  # rain
            h.set_all((102, 204, 255), 150)
        elif 700 > weather_code > 600:  # snow
            h.set_all((131, 114, 110), 50)
        elif 800 > weather_code >= 700:  # atmosphere
            h.set_all((100, 93, 91), 0)
        elif weather_code == 800:  # clear sky
            h.make_sunny(value=hour_data['temp'], min_input=0, max_input=20)
            # h.make_sunny(value=randint(70, 100))
        elif 900 > weather_code > 800:  # clouds
            h.set_all((50, 50, 50), 0)
        return weather_code
    except:
        print('weather hardware parsed')


def social_parse(rating):
    pos_percentage = rating[0]
    try:
        if pos_percentage <= 10:
            h.make_thunder()
        elif pos_percentage <= 30:
            h.set_all((153, 102, 51), 255)
        elif pos_percentage <= 50:
            h.set_all((153, 102, 51), 100)
        elif pos_percentage <= 60:
            h.set_all((153, 102, 51), 0)
        elif pos_percentage > 60:
            h.make_sunny(pos_percentage)
    except:
        print('social hardware parsed')


class Program:
    def __init__(self, settings):
        self.settings = settings
        self.SocialConnect = SocialConnect("bddae9b9df86095e0d4b9908a7a9b622", settings=self.settings)
        self.WeatherConnect = WeatherConnect("f71af11b8e02b30c2ed988487f0dd533", settings=self.settings)
        self.MQTT = MQTT("pacotinie@gmail.com", "Bepperking!")
        self.MQTT.subscribe_topic("pacotinie@gmail.com/rpi")
        self.hourly_weather = []

    def refresh_api(self):
        if self.settings.mode == "weather":
            return self.handle_weather()
        if self.settings.mode == "social":
            rating = self.get_current_social_rating()
            social_parse(rating)

    def check_messages(self):
        if len(self.MQTT.messages) > 0:
            return self.MQTT.retrieve_message()
        return None

    def process_messages(self, msg):
        # mqtt message is constructed as -> type|value
        msg_split = msg.split("|")
        if len(msg_split) > 1:
            msg_type = msg_split[0]
            value = msg_split[1]
            if msg_type == "request":
                if value == "settings":
                    self.MQTT.send_message(str(self.settings.to_json()))
                elif value == "refresh":
                    self.refresh_api()
                    self.MQTT.send_message("successfully refreshed")
                elif hasattr(self.settings, value):
                    self.MQTT.send_message(getattr(self.settings, value))

            elif msg_type == "settings":  # save all settings at once
                value = value.replace("'", '"')  # single quotes to double for json parser
                try:
                    self.settings.save_settings_json(json.loads(value))
                    self.settings.save_to_file()
                    change_interval_task('api-handling', self.settings.refresh_interval, program=self)
                    h.update_brightness()
                except ValueError as e:
                    self.MQTT.send_message("invalid json")

            else:  # save specific setting
                if hasattr(self.settings, msg_type):
                    setattr(self.settings, msg_type, value)
                    self.settings.save_to_file()
                    if msg_type == "mode" or msg_type == "refresh_interval":
                        change_interval_task('api-handling', self.settings.refresh_interval, program=self)
                    if msg_type == "brightness":
                        h.update_brightness()
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
                if hour_of_estimation_timezoned > now_with_future_forecast_time:
                    print(hour_of_estimation)
                    return weather_parse(hour_of_estimation)
        return False

    def get_current_social_rating(self):
        posts_obj = self.SocialConnect.fetch_data()
        return self.SocialConnect.calc_avg_sentiment(posts_obj)


if __name__ == "__main__":
    run_program()
