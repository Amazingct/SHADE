from concurrent import futures
import time
import grpc
import ShadeShell_pb2
import ShadeShell_pb2_grpc
import socket   


channel = grpc.insecure_channel("localhost:50051")
ShadeShell = ShadeShell_pb2_grpc.ShadeShellStub(channel)

rx = ShadeShell.ProcessCommand(ShadeShell_pb2.command(command="list"))
print(rx)