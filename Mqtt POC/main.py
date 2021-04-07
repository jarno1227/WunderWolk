import mqtt
import settings
import time
set1 = settings.Settings()
messageHandler = mqtt.MQTT("pacotinie@gmail.com", "Bepperking!", set1)

print(set1.testValue)
print("yooooo")
messageHandler.subscribe_topic("pacotinie@gmail.com/settings")

while True:
    time.sleep(10)

    while len(messageHandler.messages) != 0:
        msg = messageHandler.retrieve_message()
        msg = msg[1:]
        msg = msg[:-1]
        splitted = msg.split(":")
        if splitted[0] == "MOOD":
            set1.mood[int(splitted[1])] = splitted[2]
            print(set1.mood)