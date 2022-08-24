import paho.mqtt.client as mqtt 
from random import randrange, uniform
import time
import json
import os
mqttBroker ="localhost"
port = 1883




class node:
    def __init__(self, device_type, device_name):
        self.type = device_type
        self.name = device_name
        self.log = device_name + "/log"
        self.command = device_name + "/command"
        self.client = mqtt.Client(device_name)
        self.client.connect(mqttBroker, port)
        self.client._on_message = self.on_message
        self.client.on_subscribe = self.on_subscribe
        self.client.subscribe(self.command)
        self.success={"subcribe":False}
        self.last_log = ["None"]
        self.client.loop_start()
    
    def __repr__(self) -> str:
        return self.name +"-->"+ self.type
        
    def on_message(self,client, userdata, message):
        if len(self.log)>10:
            self.last_log.pop(0)
        self.last_log.append (json.loads(message.payload))

    def on_subscribe(self, client, userdata, mid, granted_qos):
        self.success["subcribe"] = True
        
    def get_log(self):
        time.sleep(3)
        return self.last_log[-1]
    
    def begin(self):
        self.client.loop_start()
        
    def end(self):
        self.client.loop_stop()
        
        
    def talk(self, message):
        self.client.publish(self.command,message)


def load_devices(dir = os.path.join("MainController","devices.json")):
    all_devices = {}
    with open(dir, "rb") as devices:
        devices = json.load(devices)
    
    for id, info in devices.items():
        n = node(info["type"],info["name"])
        all_devices.update({info["name"]:n})
        
    return all_devices

# receive data from client
all_devices = load_devices()
print(all_devices)
print()
while True:
    try:
        message = input("user@sha-de:>> ")
        _in = message.split(" ")
        message = {_in[1]:_in[2]}
        all_devices[_in[0]].talk(json.dumps(message))
        
        response = all_devices[_in[0]].get_log()
        print("client:>>", response)
        print("")
      
    except Exception as e:
        print(e)
