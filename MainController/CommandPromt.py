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

logs = ShadeShell.StreamLog(ShadeShell_pb2.command(command="sitting-room"))
for log in logs:
    print(log.log)



# def chat_with_shell():
#     while True:
#         command = input("command: >> ")
#         if command == "add":
#             name = input("name: >> ")
#             type = input("type: >> ")
#             child = input("child (sperate with space): >> ")
#             child = child.split(" ")
#             new = {"type":type, "name":name, "child":child}
#             command_to_send = ShadeShell_pb2.command(command="add "+json.dumps(new))
#         else:
#             command_to_send = ShadeShell_pb2.command(command = command)
#         yield command_to_send
#         if command == "quit":
#             break
#         time.sleep(3)

# responses = ShadeShell.ShellChat(chat_with_shell())
# for response in responses:
#     print("user@sha-de: >> ", json.loads(response.response)["response"])