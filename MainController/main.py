import socket
from time import sleep
import os
import threading as t
pwd = str(os.getcwd())
path = pwd + "/configurations/"
HOST = ''
PORT = 65433  # Port to listen on (non-privileged ports are > 1023) for client devices


def bind():
    global s
    s = socket.socket()
    s.bind((HOST, PORT))


try:
    bind()
except:
    s.close()
    sleep(3)
    bind()

s.listen(5)
devices = []



def start_client_connection():
    conn, addr = s.accept()
    s.setblocking(1)  # prevent timeout
    return conn, addr


def send_to_client(device, state, remove=None):
        rxx = None
        # if it takes more than 3 seconds to receive response from client, it means client has disconnected
        def count():
            timer = 0
            while timer < 4:
                sleep(1)
                timer = timer + 1
            if rxx == None and remove != None:
                device.close()
                print(" device closed")

        t.Thread(target=count).start()

        try:
            device.send(str.encode(str(state)))
            rxx = str(device.recv(1024), "utf-8")
            return rxx
        except Exception as e:
            device.close()
            return rxx
        
        
        
        
        
# MAIN SECTION

bind()
device, addr = start_client_connection()
print("connected to", addr)

while True:
    try:
        message = input(" user@sha-de:>> ")
        response = send_to_client(device, message)
        print("device:>>", response)
      
    except Exception as e:
        print(e)
        device, addr = start_client_connection()
        print("connected to", addr)
        continue
        
        
        