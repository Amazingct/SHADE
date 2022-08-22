try:
    import usocket as socket
except:
    import socket

#from machine import Pin
import network, time
import esp

esp.osdebug(None)
import gc

gc.collect()
time.sleep(2)

ssid = "shade"
password = "shade123"
hub = network.WLAN(network.STA_IF)
hub.active(True)
hub.connect(ssid, password)

print('Connection successful')
print(hub.ifconfig())

time.sleep(2)


