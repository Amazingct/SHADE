import machine
import json
from random import randrange, uniform

led = machine.Pin(2, machine.Pin.OUT)
children = {"light":"0", "temperature":""}
last_message = 0
message_interval = 1
counter = 0

def switch(command):
    try:
        if command["light"] == "1":
            led.on()
            children.update({"light":"1"})
        elif command["light"] == "0":
            led.off()
            children.update({"light":"0"})
    except Exception as e:
        client.publish("debug", json.dumps(command.update({"error":e})))
        
def update_children():
    children["temperature"] =  uniform(20.0, 60.0)

def sub_cb(topic, msg):
  print((topic, msg))
  if topic == bytes(name+ '/command', "utf-8"):
    msg = json.loads(msg)
    print('ESP received message', str(msg))
    switch(msg)
    


def connect_and_subscribe():
  global client_id, mqtt_server, topic_sub
  client = MQTTClient(client_id, mqtt_server)
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(topic_sub)
  print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()

try:
  client = connect_and_subscribe()
except OSError as e:
  restart_and_reconnect()


while True:
  try:
    client.check_msg()
    if (time.time() - last_message) > message_interval:
      update_children()
      msg = json.dumps(children)
      client.publish(topic_pub, msg)
      last_message = time.time()
      counter += 1
  except OSError as e:
    restart_and_reconnect()
