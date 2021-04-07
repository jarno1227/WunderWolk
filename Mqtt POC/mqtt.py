import paho.mqtt.client as mqtt
import settings


class MQTT:
    def __init__(self, user, pw, set1):
        self.user = user
        self.pw = pw
        self.set1 = set1
        self.messages = []

        self.mqttc = mqtt.Client()
        self.mqttc.username_pw_set(user, pw)
        self.mqttc.on_message = self.on_message
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_publish = self.on_publish
        self.mqttc.on_subscribe = self.on_subscribe
        self.mqttc.connect("maqiatto.com", 1883, 60)
        self.mqttc.loop_start()

    def on_connect(self, mqttc, obj, flags, rc):
        print("rc: " + str(rc))

    def on_message(self, client, userdata, msg):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
        message = str(msg.payload)
        message = message[2:]
        message = message[:-1]


        if message[0] == '#' and message[-1] == '%':
            self.messages.append(message)
            print(self.messages)
        else:
            print("Wrongly formatted message. (start with a # and end with a %)")

        try:
            self.set1.testValue = int(message)
        except:
            pass

    def on_publish(self, mqttc, obj, mid):
        print("mid: " + str(mid))

    def on_subscribe(self, mqttc, obj, mid, granted_qos):
        print("Subscribed: " + str(mid) + " " + str(granted_qos))

    def on_log(self, mqttc, obj, level, string):
        print(string)

    def send_message(self, topic, message):
        self.mqttc.publish(topic, message, qos=0, retain=False)

    def subscribe_topic(self, topic):
        self.mqttc.subscribe(topic, 0)

    def retrieve_message(self):
        return self.messages.pop(0)
