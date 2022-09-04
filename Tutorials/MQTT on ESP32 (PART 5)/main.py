import time
import machine
from umqttsimple import MQTTClient
from random import randrange, uniform
import ubinascii

mqtt_server = "192.168.0.132"
name = "office"

topic_sub =name+ '/command' #bathroom/command
topic_pub = name+ '/log' #bathroom/log

def on_message(topic, msg):
  if topic == bytes(name+ '/command', "utf-8"):
    print('ESP received message', str(msg))

client_id = ubinascii.hexlify(machine.unique_id())
client = MQTTClient(client_id, mqtt_server)
client.set_callback(on_message)
client.connect()
client.subscribe(topic_sub)
print('Connected to {} MQTT broker, subscribed to {} topic'.format(mqtt_server, topic_sub))
 


while True:
    client.check_msg()
    msg = uniform (20.5, 60.5)
    msg = str(msg)
    client.publish(topic_pub, msg)
    time.sleep(3)

