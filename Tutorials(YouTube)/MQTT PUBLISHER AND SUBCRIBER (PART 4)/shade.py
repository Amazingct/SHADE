import paho.mqtt.client as mqtt
import time

ip = "192.168.1.100"
port = 1883 


shade = mqtt.Client("office")
shade.connect(ip)

# subcribe

def message_rx(client, userdata, message):
    print("I just recived this value", message.payload.decode("utf-8"), "*C")


shade.subscribe("sitting-room/log")
shade._on_message=message_rx

shade.loop_forever()

