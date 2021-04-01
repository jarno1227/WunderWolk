import paho.mqtt.client as mqtt
import settings


class MQTT:
    def __init__(self, username, password, host, set1):
        self.username = username
        self.password = password
        self.host = host
        self.set1 = set1


    def on_connect(mqttc, obj, flags, rc):
        print("rc: " + str(rc))

    def on_message(self, obj, msg):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
        message = str(msg.payload)
        message = message[2:]
        message = message[:-1]
        self.set1.testValue = int(message)

    def on_publish(mqttc, obj, mid):
        print("mid: " + str(mid))

    def on_subscribe(mqttc, obj, mid, granted_qos):
        print("Subscribed: " + str(mid) + " " + str(granted_qos))

    def on_log(mqttc, obj, level, string):
        print(string)



    # If you want to use a specific client id, use
    # mqttc = mqtt.Client("yo-man-bro-ik-ben-het")
    # but note that the client id must be unique on the broker. Leaving the client
    # id parameter empty will generate a random id for you.
    mqttc = mqtt.Client()
    mqttc.username_pw_set("pacotinie@gmail.com", "Bepperking!")
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_subscribe = on_subscribe
    # Uncomment to enable debug messages
    # mqttc.on_log = on_log
    mqttc.connect("maqiatto.com", 1883, 60)
    mqttc.subscribe("pacotinie@gmail.com/settings", 0)

    mqttc.loop_start()
