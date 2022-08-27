from concurrent import futures
import json
import time
import grpc
import ShadeShell_pb2
import ShadeShell_pb2_grpc
import socket   


channel = grpc.insecure_channel("127.0.1.1:50054")
ShadeShell = ShadeShell_pb2_grpc.ShadeShellStub(channel)

rx = ShadeShell.ProcessCommand(ShadeShell_pb2.command(command="list"))
rx = json.loads(rx.response)

for device in rx["response"]:
    print(device)