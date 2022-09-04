from ShadeVision import VisionFromMqtt, PersonDetection
import cv2 as cv
import paho.mqtt.client as mqtt
import time

ip = "192.168.0.132"
port = 1883
node = mqtt.Client("vision")
node.connect(ip)




MQTT_BROKER = "192.168.0.132"
MQTT_RECEIVE = "office/camera/frame"
person = PersonDetection()
vision = VisionFromMqtt(MQTT_BROKER, MQTT_RECEIVE)

while True:
    frame = vision.getFrame()
    frame, result = person.detect(frame)
    if result is not None:
        vision.publishObjects(result["class"])
    else:
        vision.publishObjects([])
    cv.imshow("Office", frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break