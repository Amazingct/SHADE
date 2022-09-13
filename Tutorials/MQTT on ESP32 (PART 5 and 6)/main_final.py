import time
import machine
from machine import Pin
import json
import ubinascii
from umqttsimple import MQTTClient
from random import randrange, uniform

led = Pin(2, Pin.OUT)

mqtt_server = "192.168.0.132"
name = "office"
children = {"light":"0", "temperature":"0"}

topic_sub =name+ '/command' #master-room/command
topic_pub = name+ '/log' #bathroom/log

def on_message(topic, msg):
  if topic == bytes(name+ '/command', "utf-8"):
    command = json.loads(msg)
    print(command)
    
    if "light" in command.keys():
        if command["light"] == "1":
            print("turn on led")
            led.on()
            children.update({"light":"1"})
        else:
            print("turn off led")
            led.off()
            children.update({"light":"0"})
    

client_id = ubinascii.hexlify(machine.unique_id())
client = MQTTClient(client_id, mqtt_server)
client.set_callback(on_message)
client.connect()
client.subscribe(topic_sub)
print('Connected to {} MQTT broker, subscribed to {} topic'.format(mqtt_server, topic_sub))
 


while True:
    client.check_msg()
    temp = uniform (20.5, 60.5)
    children.update({"temperature":temp})
    client.publish(topic_pub, json.dumps(children))
    #time.sleep(2)
    



