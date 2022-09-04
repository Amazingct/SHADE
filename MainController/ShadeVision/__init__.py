import base64
import cv2 as cv
import numpy as np
import paho.mqtt.client as mqtt
import torch,json
import os,numpy as np
import cv2
import os

def you_downloader(link, filename = 'output', path_location = 'videos', fileformat = '.mp4'):
    "you-get --itag=18 -o videos -O trial 'https://www.youtube.com/watch?v=jNQXAC9IVRw'" #download as .mp4

    if fileformat == '.mp4':
        data = "you-get --itag=18 -o {0} -O {1} {2}".format(path_location, filename, link)
    else:
        data = "you-get -o {0} -O {1} {2}".format(path_location, filename, link)

    try:
        os.system(data)
        return path_location+"/"+filename+fileformat, True
    except Exception as e:
        print(e)
        print("Something went wrong, Ensure you-get is installed on your system")

        return "", False


url = "https://drive.google.com/file/d/1zKOPjD--hbC4sbIJhjPh3wHxxgkkgjIs/view?usp=sharing"

workin_dir = os.getcwd()
path_location =os.path.join(workin_dir,"person.pt")
model=None

if os.path.exists(path_location):
    print("model file for {} detection exists".format("person"))
else:
    you_downloader(url, filename="person", path_location=workin_dir, fileformat='.pt')
    print('downloaded model file for {} detection...'.format("person"))

model=torch.hub.load('ultralytics/yolov5', 'custom', path=path_location)  # local model # local model



def RecognisePerson(face_frame):
   pass # start with you and sayo

def RecogniseAction_Emotion(full_body_frame):
    pass # standing, sitting, happy, sad, angry, scared, surprised, neutral

def DetectFace(frame):
    face_cascade = cv.CascadeClassifier('MainController\ShadeVision\haarcascade_face_default.xml')
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    return faces

def person(npimg):
    original = npimg
    imgs = [npimg[..., ::-1]]
    # Inference
    results = model(imgs).xyxy[0].cpu().numpy()
    allperson = {'bb': [], 'confidence': [], 'class': [], 'cropped': []}
    if len(results)> 0:
        for p in results:
            if p[-1] == 0:
                x, y, x1, y1 = [round(i) for i in p[:4]]
                allperson["bb"].append([x, y, x1-x, y1-y])
                allperson["confidence"].append(p[4])
                name = "person"
                action = "standing/unknown"
                allperson["class"].append({name:action})
                allperson["cropped"].append(original[y:y1, x:x1])
        return allperson
    else:
        return None

def plot_one_box(frame, bb, color=(128, 128, 128), label=None, line_thickness=3):
    x,y,w,h = bb
    pt1 = (x, y)
    pt2 = (x + w, y + h)
    frame = cv2.rectangle(frame, pt1, pt2, color, 2)
    frame = cv2.putText(frame, label, pt1, cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, line_thickness)
    return frame


def plot_many_box(frame, bbs, color=(128, 128, 128), label=None, line_thickness=3):

    if label==None:
        label = label*len(bbs)
    else:
        label = [list(person.keys())[0] for person in label]
        #print(label)
    for i, bb in enumerate(bbs):
        x, y, w, h = bb
        pt1 = (x, y)
        pt2 = (x + w, y + h)
        frame = cv2.rectangle(frame, pt1, pt2, color, 2)
        frame = cv2.putText(frame, label[i], pt1, cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, line_thickness)
    return frame


def local_2_global(local_point,inner_bb):
    x,y,w,h=local_point
    i_x,i_y, i_w, i_h =inner_bb
    X = x+i_x
    Y = y+i_y

    X2 = (x+w)+(i_x)
    Y2 = (y+h)+(i_y)
    return X,Y,X2,Y2


class VisionFromMqtt:
    def __init__(self, mqttBroker, mqttReceive):
        self.mqttBroker = mqttBroker
        self.mqttReceive = mqttReceive
        self.frame = np.zeros((240, 320, 3), np.uint8)
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.mqttBroker)
        self.client.loop_start()
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe(self.mqttReceive)
    def on_message(self, client, userdata, msg):
        # Decoding the message
        img = base64.b64decode(msg.payload)
        # converting into numpy array from buffer
        npimg = np.frombuffer(img, dtype=np.uint8)
        # Decode to Original Frame
        self.frame = cv.imdecode(npimg, 1)
    def publishObjects(self, objects):
        to_send = {"persons":[], "actions":[], "emotions":[]}
        for obj in objects:
            to_send["persons"].append(list(obj.keys())[0])
            to_send["actions"].append(list(obj.values())[0].split("/")[0])
            to_send["emotions"].append(list(obj.values())[0].split("/")[1])
        self.client.publish(self.mqttReceive[:-6]+"/log", json.dumps(to_send))
    def getFrame(self):
        return self.frame
    def stop(self):
        self.client.loop_stop()



class VisionToMqtt:
    def __init__(self, mqttBroker, mqttSend):
        self.mqttBroker = mqttBroker
        self.mqttSend = mqttSend
        self.client = mqtt.Client()
        self.client.connect(self.mqttBroker)
    def sendFrame(self, frame):
        _, buffer = cv.imencode('.jpg', frame)
        jpg_as_text = base64.b64encode(buffer)
        self.client.publish(self.mqttSend, jpg_as_text)
    def stop(self):
        self.client.disconnect()


class PersonDetection:
    def __init__(self):
        pass
    def detect(self, frame):
        results = person(frame)
        if results is not None:
            frame = plot_many_box(frame, results["bb"], color=(128, 128, 128), label=results["class"], line_thickness=3)
        return frame, results
        

