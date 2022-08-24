import machine
import json
led = machine.Pin(2, machine.Pin.OUT)

def switch(command):
    if command["light"] == "on":
        led.on()
        client.publish(topic_pub, json.dumps({"status":"light on"}))
    elif command["light"] == "off":
        led.off()
        client.publish(topic_pub, json.dumps({"status":"light off"}))
    

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
    #if (time.time() - last_message) > message_interval:
      #msg = b'Hello #%d' % counter
      #client.publish(topic_pub, msg)
      #last_message = time.time()
      #counter += 1
  except OSError as e:
    restart_and_reconnect()
