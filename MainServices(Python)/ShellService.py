from ast import While
from distutils.log import debug
from http import client
from re import T
import threading
import paho.mqtt.client as mqtt 
from random import randrange, uniform
import time
import json
import os
from concurrent import futures
import time
import grpc
from GRPC import ShadeShell_pb2
from GRPC import ShadeShell_pb2_grpc
import socket   
mqttBroker ="192.168.0.132"

port = 1883

system = ["list", "add", "remove", "help", "exit"]
devices_json = os.path.join("MainController","Configurations","devices.json")

def date_time():
    dnode = mqtt.Client("vision")
    dnode.connect(mqttBroker, port)
    while True:
        dt =  time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())
        dt = dt.split(" ")
        to_send = json.dumps({"date":dt[0], "time":dt[1][:-3]})
        #to_send = json.dumps(dict(zip(["year","month","day","hour","minute","second"],dt.split("-"))))
        dnode.publish("date-time/log", to_send)
        
threading.Thread(target=date_time).start()

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
        return self.name + " --> "+ "type: " + str(self.type) + ", children: " + str(self.children)

    def on_message(self,client, userdata, message):
        if len(self.last_log)>10:
            self.last_log.pop(0)
        self.last_log.append (json.loads(message.payload))
        

    def on_subscribe(self, client, userdata, mid, granted_qos):
        self.success["subcribe"] = True
        
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

def remove_device(device_name, dir = devices_json):
    global all_devices
    try:
        # remove device from devices.json
        with open(dir, "rb") as devices:
            devices = json.load(devices)
        devices.pop(device_name)
        with open(dir, "w") as new_devices:
            json.dump(devices, new_devices, indent=4)
        # remove device from all_devices
        all_devices.pop(device_name)
        return True, "Device removed"
    except Exception as e:
       return False, e

def add_device(device_type, device_name,children, dir = devices_json):
    global all_devices
    try:
        with open(dir, "rb") as devices:
            devices = json.load(devices)
        devices.update({device_name:{"type":device_type, "name":device_name, "child":children}})
        with open(dir, "w") as new_devices:
            json.dump(devices, new_devices, indent= 4)

        # add device to all_devices
        all_devices.update({device_name:node(device_type,device_name,children)})
        return True, "Device added"

    except Exception as e:
        return False, e

def load_devices(dir = devices_json):
    global all_devices
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
    print("recived", message)
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
            print(_in)
            response = all_devices[_in[1]].get_log(child=_in[2])

        else:
            response = "sorry, i don't understand"
           
        print("response", response)
        return json.dumps({"status": "success", "response": response})
    except Exception as e:
        print(response, e)
        return  json.dumps({"status": "error", "response":str(e)})
# create class to service all function called - inherit from grpc

class ShadeShellServicer(ShadeShell_pb2_grpc.ShadeShellServicer):

    def ProcessCommand(self, request, context):
        # request parameter holds the parameter from the function call
        response = CommandMe(request.command)
        reply = ShadeShell_pb2.response(response=response)
        return reply

    def StreamLog(self, request, context):
        print("streaming started")
        # keep streaming until client disconnects
        try:
            while True:
                log = all_devices[request.command].get_log()
                debug = {}
                log = json.dumps(log)
                debug = json.dumps(debug)
                yield ShadeShell_pb2.log(log=log, debug=debug)
                time.sleep(1)
                if context.is_active():
                    print("streaming")
                else:
                    print("client disconnected")
                    break
            print("streaming stopped")
        except Exception as e:
            print(e)
        
    def ShellChat(self, request_iterator, context):
        print("chat started")
        try:
            while True:
                for request in request_iterator:
                    if request.command == "quit":
                        assert False # quit the loop 
                    response = CommandMe(request.command)
                    yield ShadeShell_pb2.response(response=response)
        
        except Exception as e:
            print(e)
            print("chat ended")

def serve():
    hostname=socket.gethostname()   
    IPAddr=socket.gethostbyname(hostname)   
    print("Your Computer Name is:"+hostname)   
    print("Your Computer IP Address is:"+IPAddr) 

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ShadeShell_pb2_grpc.add_ShadeShellServicer_to_server(ShadeShellServicer(), server)
    server.add_insecure_port(IPAddr+":50054")
    server.start()
    print("SERVICE STARTED")
    server.wait_for_termination()


    
if __name__ == "__main__":
    serve()

