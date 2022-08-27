from concurrent import futures
from distutils.cmd import Command
import json
import time
import grpc
import ShadeShell_pb2
import ShadeShell_pb2_grpc
import socket   


channel = grpc.insecure_channel("192.168.56.1:50054")
ShadeShell = ShadeShell_pb2_grpc.ShadeShellStub(channel)

# rx = ShadeShell.ProcessCommand(ShadeShell_pb2.command(command="set sitting_room light off"))
# rx = json.loads(rx.response)

# print(rx["response"])

logs = ShadeShell.StreamLog(ShadeShell_pb2.command(command="sitting_room"))
for log in logs:
    print(log.log)
                