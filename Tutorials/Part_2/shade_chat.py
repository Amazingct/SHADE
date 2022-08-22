import socket
from time import sleep
import os
import threading as t

# set port to 65433 and ip to the ip of the controller
HOST = ''
PORT = 65433  # Port to listen on (non-privileged ports are > 1023) for client devices


# prepare socket
s = socket.socket()
s.bind((HOST, PORT))
s.listen(5)

# accept connection from client
device, addr = s.accept()
s.setblocking(1)  # prevent timeout
print("connected to", addr)

# receive data from client
while True:
    try:
        message = input("user@sha-de:>> ")
        device.send(str.encode(str(message)))
        response = str(device.recv(1024), "utf-8")
        print("client:>>", response)
        print("")
      
    except Exception as e:
        s.close
        
        
        