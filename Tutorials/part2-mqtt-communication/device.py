import paho.mqtt.client as mqtt
from random import randrange, uniform
import time

ip = "192.168.0.132"
port = 1883


node = mqtt.Client("sitting room")
node.connect(ip)

topic = "temperature"

while True:
    temp = uniform(20.0, 31.0)
    node.publish(topic, temp)
    time.sleep(3)


