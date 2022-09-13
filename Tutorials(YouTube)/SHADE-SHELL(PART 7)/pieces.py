import json
d = { "bathroom": 
    { "name": "bathrrom", "type": [
                "switch",
                "sensor"
            ],
            "child": [
                "light",
                "temperature"
            ]
        }
    }

new = json.dumps(d)

command = "set sitting-room light on"
print(command.split(" "))

['set', 'sitting-room', 'light', 'on']