import paho.mqtt.client as mqtt 
import json
import os
import time
mqttBroker ="192.168.1.100"
port = 1883

system = ["list", "add", "remove", "help", "exit"]
devices_json = "devices.json"


class node:
    def __init__(self, device_type, node_name, children=[]):
        self.children = children
        self.type = device_type
        self.name = node_name
        self.log = node_name + "/log"
        self.command = node_name + "/command"
        self.client = mqtt.Client(node_name)
        self.client.connect(mqttBroker, port)
        self.client.subscribe(self.log)
        self.client._on_message = self.on_message
        self.last_log = [None]
        self.client.loop_start()
    

    def represent(self):
        return self.name + " --> "+ "type: " + str(self.type) + ", children: " + str(self.children)

    def on_message(self, client, userdata, message):
        #print("Message received: " + str(message.payload.decode("utf-8")))
        if len(self.last_log)>10:
            self.last_log.pop(0)
        self.last_log.append (json.loads(message.payload))
        
        
    def get_log(self, index=-1, child=""):
        #time.sleep(2)
        if child == "":
            return self.last_log[index]
        else:
            return self.last_log[index][child]
        
    
    def begin(self):
        self.client.loop_start()
        
    def end(self):
        self.client.loop_stop()
        
        
    def talk(self, message):
        self.client.publish(self.command,message)

def remove_device(node_name, dir = devices_json):
    # remove device from devices.json
    with open(dir, "rb") as devices:
        devices = json.load(devices)
    devices.pop(node_name)

    with open(dir, "w") as new_devices:
        json.dump(devices, new_devices, indent=4)
    return True, "Device removed"
   
def add_device(device_type, node_name,children, dir = devices_json):
    try:
        with open(dir, "rb") as devices:
            devices = json.load(devices)
        devices.update({node_name:{"type":device_type, "name":node_name, "child":children}})
        with open(dir, "w") as new_devices:
            json.dump(devices, new_devices, indent=4)

        # add device to all_devices
        all_devices.update({node_name:node(device_type,node_name,children)})
        return True, "Device added"

    except Exception as e:
        return False, e

def load_devices(dir = devices_json):
    all_devices = {}
    with open(dir, "rb") as devices:
        devices = json.load(devices)
        
    for id, info in devices.items():
        n = node(info["type"],id,children=info["child"])
        all_devices.update({info["name"]:n})
    return all_devices

def CommandMe(message):
    c = message.split(" ")[0]
    print("recived :", message)

    if c in system:
        if c == "list":
            if len(all_devices) == 0:
                response = "No devices connected"
            else:
                response = []
                for device in all_devices.values():
                    response.append( device.represent() )
            
        elif c == "add":
            message = message[4:] #pick the json part of the message
            json_message = json.loads(message)
            
            print("adding device", json_message["name"])
            device_type = json_message["type"]
            node_name = json_message["name"]
            children = json_message["child"]

            n = node(device_type,node_name,children)
            all_devices.update({node_name:n})
            sucess , info = add_device(device_type, node_name, children)
            response = "device added"
        

        elif c == "remove":
            node_name = message[7:]
            all_devices[node_name].end()
            del all_devices[node_name]
            sucess , info = remove_device(node_name)
            response = "device removed"

        elif c == "help":
            response = ["list", "add", "remove", "help", "exit"]

    elif c =="set":
        _in = message.split(" ")
        if _in[3] == "on":
            _in[3 ]="1"
        elif _in[3] == "off":
            _in[3] = "0"
        message = {_in[2]:_in[3]}
        all_devices[_in[1]].talk(json.dumps(message))
        # response = all_devices[_in[1]].get_log()
        response = _in[1] + " " + _in[2] + " set to " + _in[3]

    elif c =="get":
        _in = message.split(" ")
        
        response = all_devices[_in[1]].get_log(child=_in[2])

    else:
        response = "sorry, i don't understand"
        
    return {"status": "success", "response": response}


# receive data from client
all_devices = load_devices()

office = {
        "name": "office",
        "type": [
            "switch",
            "sensor"
        ],
        "child": [
            "light",
            "temperature"
        ]
    }

office = json.dumps(office)

while True:
    message = input("Enter command: ")
    if message == "exit":
        break
    response = CommandMe(message)
    print(response)


