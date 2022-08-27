import paho.mqtt.client as mqtt 
from random import randrange, uniform
import time
import json
import os
from concurrent import futures
import time
import grpc
from GRPC import shell_pb2
from GRPC import shell_pb2_grpc
import socket   
mqttBroker ="192.168.0.132"

port = 1883

system = ["list", "add", "remove", "help", "exit"]


class node:
    def __init__(self, device_type, device_name, children=[]):
        self.children = children
        self.type = device_type
        self.name = device_name
        self.log = device_name + "/log"
        self.command = device_name + "/command"
        self.client = mqtt.Client(device_name)
        self.client.connect(mqttBroker, port)
        self.client._on_message = self.on_message
        self.client.on_subscribe = self.on_subscribe
        self.client.subscribe(self.log)
        self.success={"subcribe":False}
        self.last_log = ["None"]
        self.client.loop_start()
    
    def __repr__(self) -> str:
        return self.name + " --> "+ "type: " + self.type + ", children: " + str(self.children)

    def represent(self) -> str:
        return self.name + " --> "+ "type: " + self.type + ", children: " + str(self.children)

    def on_message(self,client, userdata, message):
        if len(self.log)>10:
            self.last_log.pop(0)
        self.last_log.append (json.loads(message.payload))

    def on_subscribe(self, client, userdata, mid, granted_qos):
        self.success["subcribe"] = True
        
    def get_log(self, index=-1, child=""):
        time.sleep(3)
        if child == "":
            if index !=-1:
                return self.last_log
            else:
                return self.last_log[index]
        else:
            return self.last_log[index][child]
        
    
    def begin(self):
        self.client.loop_start()
        
    def end(self):
        self.client.loop_stop()
        
        
    def talk(self, message):
        self.client.publish(self.command,message)

def remove_device(device_name, dir = os.path.join("MainController","devices.json")):
    try:
        # remove device from devices.json
        with open(dir, "rb") as devices:
            devices = json.load(devices)
        devices.pop(device_name)
        with open(dir, "w") as new_devices:
            json.dump(devices, new_devices)
        # remove device from all_devices
        all_devices.pop(device_name)
  

        print("command executed sucessfully")
    except:
        print("Error:", e)


def add_device(device_type, device_name,children, dir = os.path.join("MainController","devices.json")):
    try:
        with open(dir, "rb") as devices:
            devices = json.load(devices)
        devices.update({device_name:{"type":device_type, "name":device_name, "child":children}})
        with open(dir, "w") as new_devices:
            json.dump(devices, new_devices)

        # add device to all_devices
        all_devices.update({device_name:node(device_type,device_name,children)})
       
        print("command executed sucessfully")

    except:
        print("Error:", e)

def load_devices(dir = os.path.join("MainController","devices.json")):
    all_devices = {}

    with open(dir, "rb") as devices:
        devices = json.load(devices)
    for id, info in devices.items():
        n = node(info["type"],id,children=info["child"])
        all_devices.update({info["name"]:n})

        
    return all_devices

# receive data from client
all_devices = load_devices()
print(all_devices)
def CommandMe(message):
    try:
        if message in system:
            if message == "list":
                if len(all_devices) == 0:
                    print("No devices found")
                else:
                    response = ""
                    for device in all_devices.values():
                        response = device.represent() + ","
                    return "user@sha-de:>> "+ response
            elif message == "add":
                device_type = input("type: ")
                device_name = input("name: ")
                children = input("children (seperate with space): ")
                children = children.split(" ")
                n = node(device_type,device_name,children)
                all_devices.update({device_name:n})
                add_device(device_type, device_name, children)
                response = "device added"
                return "user@sha-de:>> "+ response

            elif message == "remove":
                device_name = input("name: ")
                all_devices[device_name].end()
                del all_devices[device_name]
                remove_device(device_name)
                response = "device removed"
                return  "user@sha-de:>> "+ response

            elif message == "help":
                response = "list, addd, remove, help, exit"
                return  "user@sha-de:>> "+ response

        elif message[:3]=="set":
            _in = message.split(" ")
            message = {_in[2]:_in[3]}
            all_devices[_in[1]].talk(json.dumps(message))
            response = all_devices[_in[1]].get_log()
            return  "user@sha-de:>> "+ response
    

        elif message[:3]=="get":
            _in = message.split(" ")
            response = all_devices[_in[1]].get_log(child=_in[2])
            return  "user@sha-de:>>  "+ response   
      
    except Exception as e:
        return  e

# create class to service all function called - inherit from grpc
class ShadeShellServicer(shell_pb2_grpc.ShadeShellServicer):

    def ProcessCommand(self, request, context):
        # request parameter holds the parameter from the function call
        response = CommandMe(request.command)
        reply = shell_pb2.response(response=response)
        return reply

    def StreamLog(self, request, context):
        while True:
            yield shell_pb2.response(response=all_devices[request.device].get_log())
            time.sleep(1)


def serve():
    hostname=socket.gethostname()   
    IPAddr=socket.gethostbyname(hostname)   
    print("Your Computer Name is:"+hostname)   
    print("Your Computer IP Address is:"+IPAddr) 
    print("WAITING FOR REQUEST")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    shell_pb2_grpc.add_ShadeShellServicer_to_server(ShadeShellServicer(), server)
    server.add_insecure_port(IPAddr+":50054")
    server.start()
    server.wait_for_termination()


    
if __name__ == "__main__":
    serve()