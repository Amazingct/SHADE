import json
import os
'''
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


def load_scenes(dir = os.path.join("MainController","Configurations","scenes.json")):
    scenes = {}
    with open(dir, "rb") as scenes_file:
        scenes = json.load(scenes_file)
    return scenes


class Scene:
    def __init__(self, name, conditions, actions):
        self.name = name
        self.conditions = conditions
        self.actions = actions
