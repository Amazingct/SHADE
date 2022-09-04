# Importing Libraries
import cv2 as cv
import paho.mqtt.client as mqtt
import base64
import time

broker = "192.168.0.132"
topic= "office/camera"

cap = cv.VideoCapture(0)
client = mqtt.Client()
client.connect(broker)
try:
 while True:
  start = time.time()
  _, frame = cap.read()
  # Encoding the Frame
  _, buffer = cv.imencode('.jpg', frame)
  # Converting into encoded bytes
  jpg_as_text = base64.b64encode(buffer)
  # Publishig the Frame on the Topic home/server
  client.publish(topic, jpg_as_text)
  end = time.time()
  t = end - start
  fps = 1/t
  print(fps)
except:
 cap.release()
 client.disconnect()
