import paho.mqtt.client as mqtt
import time

ip = "192.168.0.132"
port = 1883


shade = mqtt.Client("shade")
shade.connect(ip)

# subcribe

def message_rx(client, userdata, message):
    print("I just recived this value", message.payload.decode("utf-8"), "*C")


shade.subscribe("temperature")
shade.on_message=message_rx

shade.loop_forever()

