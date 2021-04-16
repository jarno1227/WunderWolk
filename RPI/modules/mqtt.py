import paho.mqtt.client as mqtt


class MQTT:
    def __init__(self, user, pw):
        self.messages = []
        self.mqttc = mqtt.Client()
        self.mqttc.username_pw_set(user, pw)
        self.mqttc.on_message = self.on_message
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_publish = self.on_publish
        self.mqttc.on_subscribe = self.on_subscribe
        self.mqttc.connect("maqiatto.com", 1883, 60)
        self.mqttc.loop_start()
        self.app_topic = "pacotinie@gmail.com/app"

    def on_connect(self, mqttc, obj, flags, rc):
        pass
        # print("rc: " + str(rc))

    def on_message(self, client, userdata, msg):
        message = str(msg.payload.decode("utf-8"))
        self.messages.append(message)

    def on_publish(self, mqttc, obj, mid):
        pass
        # print("mid: " + str(mid))

    def on_subscribe(self, mqttc, obj, mid, granted_qos):
        pass
        # print("Subscribed: " + str(mid) + " " + str(granted_qos))

    def on_log(self, mqttc, obj, level, string):
        print(string)

    def send_message(self, message):
        self.mqttc.publish(self.app_topic, message, qos=0, retain=False)

    def subscribe_topic(self, topic):
        self.mqttc.subscribe(topic, 0)

    def retrieve_message(self):
        return self.messages.pop(0)
