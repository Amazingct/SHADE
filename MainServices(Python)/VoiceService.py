import json
import time
import grpc
from GRPC import ShadeShell_pb2
from GRPC import ShadeShell_pb2_grpc
import pyttsx3
import pyttsx3 
import speech_recognition as sr

channel = grpc.insecure_channel("192.168.56.1:50054")
ShadeShell = ShadeShell_pb2_grpc.ShadeShellStub(channel)




engine = pyttsx3.init()

def configure_voice():
    engine.setProperty('rate', 120)
    engine.setProperty('volume', 1.0)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)

def speak(text):
    engine.say(str(text))
    engine.runAndWait()
    while engine.isBusy():
        time.sleep(0.1)
        engine.stop()
 
    

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""
        try:
            said = r.recognize_google(audio)
        except Exception as e:
            print("Exception:", str(e))
            
    command = said.lower()
    
    return command


def preprocess_command(command):
    command = command.lower()
    command = command.replace("sitting room", "sitting-room")
    return command

print("Welcome to the voice assistant")
configure_voice()

def chat_with_shell():
    while True:
        
        print("voice: >> ")
        command = get_audio()
        command = preprocess_command(command)
        print(command)
        if command == "":
            time.sleep(3)
            continue
        if command == "add":
            name = input("name: >> ")
            type = input("type: >> ")
            child = input("child (sperate with space): >> ")
            child = child.split(" ")
            new = {"type":type, "name":name, "child":child}
            command_to_send = ShadeShell_pb2.command(command="add "+json.dumps(new))
        else:
            command_to_send = ShadeShell_pb2.command(command = command)
        yield command_to_send
        if command == "quit":
            break
        time.sleep(3)
        

responses = ShadeShell.ShellChat(chat_with_shell())
for response in responses:
    r = json.loads(response.response)["response"]
    print("user@sha-de: >> ", r )
    speak(r)




