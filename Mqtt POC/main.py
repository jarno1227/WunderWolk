import mqtt
import settings
import time
set1 = settings.Settings()
messageHandler = mqtt.MQTT("joe", "mamma", "maqqiato.com", set1)

print(set1.testValue)
print("yooooo")

while True:
    time.sleep(1)
    print(set1.testValue)