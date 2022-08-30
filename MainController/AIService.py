from ast import operator
import json
import os
import time
import grpc
import ShadeShell_pb2
import ShadeShell_pb2_grpc
import pandas as pd
import threading as th
'''
SCENES CONFIGURATION:

see Configurations/sences.json for more information to set up scenes

for cameras, they will be named as camera-[location] eg camera-living-room.
cameras will pusblish to the topic camera name/image and subscribe to the topic camera name/command.
when AIService receives frames from the camera, it will run person detection and action/emotion detection on the frame,
and publish the result to the topic cameraname/result.

The format of the result is a json string with the following format:
{camera-sitting-room:{"person":{person1:{"action":action1, "emotion":emotion1}, person2:{"action":action2, "emotion":emotion2}}}}

for Scene Automation involving cameras, it will be defined as:
 { "conditions": ["camera-sitting-room *person* = *emotion or action*"], "actions":["set tv netflix = romance-movie"]}:
  ---> meaning if this person is present and is doing this action or emotion, then set the tv to netflix and play a romance-movie
 
 {"conditions": ["camera-sitting-room . = *emotion or action*"], "actions":[ "set tv netflix = action-movie"]}:
    ---> meaning if any person is present and is doing this action or emotion, then set the tv to netflix and play an action-movie

 {"conditions": ["camera-sitting-room *person* = . "], "actions":["set tv netflix = action-movie"]}:
    ---> meaning if this person is present and is doing any action or emotion, then set the tv to netflix and play an action-movie

Notes:
1. You can have multiple conditions and actions
2. You can have multiple cameras/devices in the conditions
3. The . (dot) represents any person or any action or any emotion

'''
scenes_path = os.path.join(os.path.dirname(__file__), "Configurations/scenes.json")
channel = grpc.insecure_channel("192.168.56.1:50054")
ShadeShell = ShadeShell_pb2_grpc.ShadeShellStub(channel)

def load_scenes(dir = scenes_path):
    scenes = {}
    with open(dir, "rb") as scenes_file:
        scenes = json.load(scenes_file)
    return scenes


class Scene:
    def __init__(self, name, conditions, actions, record = True):
        self.name = name
        self.conditions = conditions
        self.actions = actions
        self.streams = {}


    def __repr__(self) -> str:
        return f"Scene: {self.name} --> Conditions: {self.conditions} Actions: {self.actions}"

    # add device state to table
    def add_to_record(self, node):
        pass

    def _start_streaming(self, node, condition):
        logs = ShadeShell.StreamLog(ShadeShell_pb2.command(command=node))
        for log in logs:
            self.streams.update({node:json.loads(log.log)})
            should_i_act = self.check_conditions(condition)
            self.act(should_i_act)

    def start_streaming(self):
        for condition in self.conditions:
            node = condition.split(" ")[0]
            th.Thread(target=self._start_streaming, args=(node, condition)).start()

    def act(self, should_i_act):
        if should_i_act:
            for action in self.actions:
                print("Acting Action:", action)
                ShadeShell.ProcessCommand(ShadeShell_pb2.command(command=action))
                #time.sleep(1)

    def check_conditions(self, condition):
        condition_ = condition.split(" ")
        node = condition_[0]
        child = condition_[1]
        operator = condition_[2]
        value = condition_[3]

        if node not in ["date-time","tv"]: # regular switches and sensors
            if operator == "=":
                print("Condition met:", condition)
                return float(self.streams[node][child]) == float(value)
            elif operator == ">":
                print()
                print("Condition met:", condition)
                return float(self.streams[node][child]) > float(value)
            elif operator == "<":
                print("Condition met:", condition)
                return float(self.streams[node][child]) < float(value)
            elif operator == ">=":
                print("Condition met:", condition)
                return float(self.streams[node][child]) >= float(value)
            elif operator == "<=":
                print("Condition met:", condition)
                return float(self.streams[node][child]) <= float(value)
            elif operator == "!=":
                print("Condition met:", condition)
                return float(self.streams[node][child]) != float(value)
            else:
                #print("Condition not met:", condition)
                return False
        elif node in ["date-time","tv"]: # tv and date-time are special cases, cant convert ther value to float
            pass

        elif "camera" in node: # camera is a special case, it has . (dot) as a value, so we need to check if the value is .
            pass


        


        

    def start(self):
        self.start_streaming()


    def stop(self):
        pass




if __name__ == "__main__":
    all_scenes = load_scenes()
    scenes = []
    for name, scene in all_scenes.items():
        s = Scene(scene["name"], scene["conditions"], scene["actions"])
        scenes.append(s)
        scenes[-1].start()
        print(s)

