import paho.mqtt.client as mqtt 
from random import randrange, uniform
import time
import json
import os
from concurrent import futures
import time
import grpc
import ShadeShell_pb2
import ShadeShell_pb2_grpc
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
        time.sleep(2)
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
        return True, "Device removed"
    except Exception as e:
       return False, e


def add_device(device_type, device_name,children, dir = os.path.join("MainController","devices.json")):
    try:
        with open(dir, "rb") as devices:
            devices = json.load(devices)
        devices.update({device_name:{"type":device_type, "name":device_name, "child":children}})
        with open(dir, "w") as new_devices:
            json.dump(devices, new_devices)

        # add device to all_devices
        all_devices.update({device_name:node(device_type,device_name,children)})
        return True, "Device added"

    except Exception as e:
        return False, e

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
print("-----------------------------------------")
def CommandMe(message):
    c = message.split(" ")[0]
    try:
        
        if c in system:
            if c == "list":
                if len(all_devices) == 0:
                    response = "No devices connected"
                else:
                    response = []
                    for device in all_devices.values():
                        response.append( device.represent() )
                
            elif c == "add":
                message = message[4:]
                json_message = json.loads(message)
                print("adding device", json_message["name"])
                device_type = json_message["type"]
                device_name = json_message["name"]
                children = json_message["child"]
                n = node(device_type,device_name,children)
                all_devices.update({device_name:n})
                sucess , info = add_device(device_type, device_name, children)
                response = "device added"
            

            elif c == "remove":
                device_name = message[7:]
                all_devices[device_name].end()
                del all_devices[device_name]
                sucess , info = remove_device(device_name)
                response = "device removed"


            elif c == "help":
                response = ["list", "add", "remove", "help", "exit"]
  

        elif c =="set":
            _in = message.split(" ")
            message = {_in[2]:_in[3]}
            all_devices[_in[1]].talk(json.dumps(message))
            response = all_devices[_in[1]].get_log()

    

        elif c =="get":
            _in = message.split(" ")
            response = all_devices[_in[1]].get_log(child=_in[2])
           

        return json.dumps({"status": "success", "response": response})
    except Exception as e:
        return  json.dumps({"status": "error", "response":str(e)})

# create class to service all function called - inherit from grpc
class ShadeShellServicer(ShadeShell_pb2_grpc.ShadeShellServicer):

    def ProcessCommand(self, request, context):
        # request parameter holds the parameter from the function call
        response = CommandMe(request.command)
        reply = ShadeShell_pb2.response(response=response)
        return reply

    def StreamLog(self, request, context):
        while True:
            yield ShadeShell_pb2.response(response=all_devices[request.device].get_log())
            time.sleep(1)


def serve():
    hostname=socket.gethostname()   
    IPAddr=socket.gethostbyname(hostname)   
    print("Your Computer Name is:"+hostname)   
    print("Your Computer IP Address is:"+IPAddr) 
    print("WAITING FOR REQUEST")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ShadeShell_pb2_grpc.add_ShadeShellServicer_to_server(ShadeShellServicer(), server)
    server.add_insecure_port(IPAddr+":50054")
    server.start()
    server.wait_for_termination()


    
if __name__ == "__main__":
    serve()

# a = (CommandMe("set sitting_room light off"))
# a = json.loads(a)
# print( a["response"])

# a = (CommandMe("get sitting_room light"))
# a = json.loads(a)
# print( a["response"])

# new = {"type":"switch", "name":"kitchen", "child":["light", "fan"]}
# a = (CommandMe("add "+json.dumps(new)))

# a = (CommandMe("list"))
# a = json.loads(a)
# print( a["response"])

# a = (CommandMe("remove kitchen"))
# a = json.loads(a)
# print( a["response"])

# a = (CommandMe("list"))
# a = json.loads(a)
# print( a["response"])

 
