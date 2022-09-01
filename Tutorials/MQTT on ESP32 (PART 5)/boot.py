import network
import esp
import json
esp.osdebug(None)
import gc
gc.collect()

file = open("config.json", "r")
config = json.load(file)
file.close()

ssid = config["wifi"]
password = config["wifi_password"]

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(ssid, password)

while wifi.isconnected() == False:
  pass

print('Connection successful')
print(wifi.ifconfig())
