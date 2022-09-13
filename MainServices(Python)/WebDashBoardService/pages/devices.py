import streamlit as st
from concurrent import futures
from distutils.cmd import Command
import json
import time, os
import grpc
from GRPC import ShadeShell_pb2
from GRPC import ShadeShell_pb2_grpc
from ShadeVision import VisionFromMqtt, PersonDetection
import cv2 as cv
import paho.mqtt.client as mqtt


channel = grpc.insecure_channel("192.168.56.1:50054")
ShadeShell = ShadeShell_pb2_grpc.ShadeShellStub(channel)
devices_json = os.path.join("MainController","Configurations","devices.json")
all_devices = {}

with open("E:\Projects\SHA-DE\SHADE\MainController\Configurations\devices.json", "rb") as devices:
    devices = json.load(devices)

st.write(
    
    
    """

    # ![logo] SHA-DE DASHBOARD 
    [Github](https://www.github.com/Amazingct/SHADE) | [Youtube](https://www.youtube.com/watch?v=C3DmehDGIww&list=PLQDvLS_MNLkf7i2TDSJD13QhRDkX_hE9F)

    ---
    
     
    [logo]: https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 2"
    """
)



class NodeCard:
    def __init__(self, name, type, children):
        self.name = name
        self.type = dict(zip(children, type))
        self.children = children
        self.state = dict(zip(children, ["77" for i in range(len(children))]))
        self.children_command = dict(zip(children, ["" for i in range(len(children))]))


        #update devices state
        self.update_state()

        

    def send_command(self,child):
        child = child.lower()
        state = str(self.children_command[child]).lower()
        if state == "on":
            state = "off"
        elif state == "off":
            state = "on"
        print(child, state)
        # try:
        #     response = ShadeShell.ProcessCommand(ShadeShell_pb2.command(command=command))
        # except:
        #     pass

    def update_state(self):
        pass

    def get_state(self, child):
        return self.children[child]

    def render(self):
        st.write(f"""
        
        ## {self.name.upper()}
        
        """)
        col = st.columns(len(self.children),gap="large")
        for child,state in self.children_command.items():
            col_number = self.children.index(child)
            with col[col_number]:
                st.write(f"""
                #### {child.capitalize()}
                """)
                key = self.name+"_"+child
                if self.type[child] == "switch":
                    self.children_command[child] = st.radio("LIGHT", ["ON", "OFF"], on_change=self.send_command, key=key,args=(child,))
                elif self.type[child] == "dimmer":
                    self.children_command[child] = st.slider("DIMMER", 0,10, 10, on_change=self.send_command, key=key,args=(child,))
                elif self.type[child] == "sensor":
                    st.write(f"""
                    ### **{self.state[child]}**°C
                    """)

class CameraNode:
    def __init__(self, name, broker, topic):
        self.name = name
        self.broker = broker
        self.topic = topic
        camera = VisionFromMqtt(broker, topic)

    def render(self):
        st.write(f"""
        
        ## {self.name.upper()}
        
        """)
       
        
office = NodeCard("office", ["switch", "sensor", "dimmer"], ["light", "temperature", "fan"])
sitting_room = NodeCard("sitting-room", ["switch", "sensor", "dimmer"], ["light", "temperature", "fan"])
office_camera = CameraNode("office-camera", "192.168.0.132", "office/camera/frame")
office.render()
sitting_room.render()
office_camera.render()

