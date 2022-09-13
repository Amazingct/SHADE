import time
import json
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp
esp.osdebug(None)
import gc
gc.collect()


with open("config.json", "r") as config:
    config = json.load(config)

ssid = config["wifi"]
password = config["wifi_password"]
mqtt_server = config["broker"]
name = config["name"]

client_id = ubinascii.hexlify(machine.unique_id())
topic_sub = bytes(name+ '/command', "utf-8")
topic_pub = bytes(name+ '/log', "utf-8")


station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())
