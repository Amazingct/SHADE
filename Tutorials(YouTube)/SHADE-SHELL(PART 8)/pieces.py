import paho.mqtt.client as mqtt 
mqttBroker ="192.168.1.100"
port = 30100


def on_message(self, client, userdata, message):
    print("Message received: " + str(message.payload.decode("utf-8")))


node_name = "office"
log = node_name + "/log"
command = node_name + "/command"
client = mqtt.Client(node_name)
client.subscribe(log)
client.connect(mqttBroker, port)
client._on_message = on_message
last_log = [None]
client.loop_start()
    

