# SHA-DE (SMART HOME ASSITANT AND DIGITAL ECO-SYSTEM). 
I am on a mission to make my house smart, and I would be doing almost everything from scratch. Let's do this together, let's learn together.

![SMART HOME ASSISTANT AND DIGITAL ECO-SYSTEM- SHA-DE](flow.png)

### Please Note, this is still a work in progress, kindly stay updated via the youtube playlist attached below
### YOUTUBE TUTORIALS
https://youtube.com/playlist?list=PLQDvLS_MNLkf7i2TDSJD13QhRDkX_hE9F

### MAIN FEATURES:
1. WEB DASHBOARD
2. VOICE ASSITANT/CONTROL
3. COMMAND PROMPT
4. AI-POWERED AUTOMATION (VISION AND AUTOMATION SERVICES)

### DEVICES TYPE
1. sensor: read
2. switch: read/write(1,0,on,off)
3. dimmer: read/write(0-10, on,off)
4. camera: read(person, actions, emotions, frame)
5. date-time:read(time, date)

READ: The Value can be read via the [node name]/log topic (eg: office/log)
WRITE: The value can be change via the [node name]/command topic (eg: office/command)



### CAMERA TOPICS:
1. [location]/[camera]/frame:

        eg. office/camera/frame.
        Raw frames are published here for services such as the WEBUI
2. [location]/[camera]/log:

        eg. office/camera/log.
        Results of person/action/emotion recognition are pusblished here for services such as Automation Service. 
        eg. {
            "person":["daniel", "clark"],
            "emotion":["happy", "unknown"],
            "action": ["sitting", "standing"]
        }

### DATE-TIME TOPIC:

1. date-time/log:

        Services can get time and date from this topic. The message format:
        {"date": "2022-09-13", "time": "14-20"}

        NOTE: There can only be one date-time node in the network


### NODE(DEVICES) TOPICS:
1. [location]/[log]:

        eg. office/log.
       states of devices are published here in this format:
       {"temperature": "34", "light": "1"}
2. [location]/command:

        eg. office/command.
       states of devices can be changed through this topic by pusblishing in this format:
       {"light": "1", "door":"1"}