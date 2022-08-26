import json
devices = {"name":"dan"}
with open("test.json", "w") as new_devices:
        json.dump(devices, new_devices)