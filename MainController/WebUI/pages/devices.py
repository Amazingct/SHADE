import streamlit as st
from concurrent import futures
from distutils.cmd import Command
import json
import time
import grpc
from GRPC import ShadeShell_pb2
from GRPC import ShadeShell_pb2_grpc
import os


channel = grpc.insecure_channel("127.0.1.1:50054")
ShadeShell = ShadeShell_pb2_grpc.ShadeShellStub(channel)
devices_json = os.path.join("MainController","Configurations","devices.json")
all_devices = {}

with open(devices_json, "rb") as devices:
    devices = json.load(devices)


def send_command(command):
    rx = ShadeShell.ProcessCommand(ShadeShell_pb2.command(command=command))
    rx = json.loads(rx.response)
    return rx["response"]



for id, info in devices.items():
    col1, col2 = st.columns(2, gap="small")
    with st.container():
        st.write("## {}".format(info["name"]))
        for child in info["child"]:
            st.write("### {}".format(child))
        
