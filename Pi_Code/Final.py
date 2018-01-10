from lidar_lite import Lidar_Lite
from picamera.array import PiRGBArray
from picamera import PiCamera
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import cv2
import sys
from openalprlib import Alpr
import numpy as np
from Adafruit_PWM_Servo_Driver import PWM
import json
from datetime import datetime

# from datetime import datetime (From timestamp)
# AWS Declear and setup

# python3 Final.py -e a1s6u9kqjd43mc.iot.us-west-2.amazonaws.com -r /home/pi/AWSCERT/root-CA.crt -k /home/pi/AWSCERT/Parking_Cam.private.key -c /home/pi/AWSCERT/Parking_Cam.cert.pem -t car/location
# Read in command-line parameters
parser = argparse.ArgumentParser()
parser.add_argument("-e", "--endpoint", action="store", required=True, dest="host", help="Your AWS IoT custom endpoint")
parser.add_argument("-r", "--rootCA", action="store", required=True, dest="rootCAPath", help="Root CA file path")
parser.add_argument("-c", "--cert", action="store", dest="certificatePath", help="Certificate file path")
parser.add_argument("-k", "--key", action="store", dest="privateKeyPath", help="Private key file path")
parser.add_argument("-w", "--websocket", action="store_true", dest="useWebsocket", default=False,
                    help="Use MQTT over WebSocket")
parser.add_argument("-id", "--clientId", action="store", dest="clientId", default="basicPubSub",
                    help="Targeted client id")
parser.add_argument("-t", "--topic", action="store", dest="topic", default="sdk/test/Python", help="Targeted topic")

args = parser.parse_args()
host = args.host
rootCAPath = args.rootCAPath
certificatePath = args.certificatePath
privateKeyPath = args.privateKeyPath
useWebsocket = args.useWebsocket
clientId = args.clientId
topic = args.topic

if args.useWebsocket and args.certificatePath and args.privateKeyPath:
    parser.error("X.509 cert authentication and WebSocket are mutual exclusive. Please pick one.")
    exit(2)

if not args.useWebsocket and (not args.certificatePath or not args.privateKeyPath):
    parser.error("Missing credentials for authentication.")
    exit(2)

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
if useWebsocket:
    myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId, useWebsocket=True)
    myAWSIoTMQTTClient.configureEndpoint(host, 443)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath)
else:
    myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
    myAWSIoTMQTTClient.configureEndpoint(host, 8883)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
time.sleep(1)
#######################AWS connect done##############################

######Hardware Initialization########################################

lidar = Lidar_Lite()
connected = lidar.connect(1)
# Initialise the PWM device using the default address
pwm = PWM(0x40)


def setServoPulse(channel, pulse):
    pulseLength = 1000000  # 1,000,000 us per second
    pulseLength /= 60  # 60 Hz
    print("%d us per period" % pulseLength)
    pulseLength /= 4096  # 12 bits of resolution
    print("%d us per bit" % pulseLength)
    pulse *= 1000
    pulse /= pulseLength
    pwm.setPWM(channel, 0, pulse)


pwm.setPWMFreq(60)  # Set frequency to 60 Hz

position = [225, 275, 325, 375, 425, 475, 525]
degree = [30, 50, 70, 90, 110, 130, 150]

# initialize the camera and grab a reference to the raw camera capture
alpr = Alpr("us", "/home/pi/openalpr/config/openalpr.defaults.conf", "/home/pi/openalpr/runtime_data")
if not alpr.is_loaded():
    print("Error loading OpenALPR")
    sys.exit(1)
alpr.set_top_n(20)
alpr.set_default_region("md")
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
rawCapture = PiRGBArray(camera)
# allow the camera to warmup
time.sleep(0.1)

# Json declare
return_to_AWS = {}
returnSpace = {}
Location = "SJSU West"
Row = "B"
SpaceTopic = "car/space"
Floor = 15

if connected < -1:
    print("Not Connected")
else:
    print("Lidar scan bgins")

while True:
    space = 0;
    for i in range(7):  # 7 different positions for servo motor to stop
        pwm.setPWM(0, 0, position[i])
        time.sleep(1)
        distance = lidar.getDistance()
        if (distance < 200):
            space = space + 1
        print("Currnet degree = %s" % degree[i])
        for j in range(3):  # Lidar will collect data 3 times for one position
            distance = lidar.getDistance()
            print("Distance to target = %s" % (distance))
            if (distance < 1000):
                print("Start Recognizing at position:", j + 1)
                camera.capture(rawCapture, format="bgr")
                image = cv2.cvtColor(rawCapture.array, cv2.COLOR_BGR2GRAY)
                results = alpr.recognize_ndarray(image)
                for plate in results['results']:
                    for candidate in plate['candidates']:
                        # The Prefix is not necessary for the program.
                        if (candidate['confidence'] > 85):
                            print(candidate['plate'])
                            return_to_AWS['License'] = candidate['plate']
                            # return_to_AWS['Date'] = datetime.now().strftime('%D')
                            return_to_AWS['Time'] = datetime.now().strftime('%H:%M:%S')
                            return_to_AWS['Location'] = Location
                            return_to_AWS['Floor'] = Floor
                            return_to_AWS['Row'] = Row
                            # return_to_AWS['Confidence'] = candidate['confidence']
                            print("This is the successful Json.")
                            print(json.dumps(return_to_AWS))
                            myAWSIoTMQTTClient.publish(topic, json.dumps(return_to_AWS), 1)
                            print("Updated License successfully")
                rawCapture.truncate(0)
                print("Scan Next Position")
                time.sleep(5)
    returnSpace['Location'] = Location
    returnSpace['Row'] = Row
    returnSpace['Time'] = datetime.now().strftime('%H:%M:%S')
    returnSpace['Floor'] = Floor
    returnSpace['Available_Space'] = space
    print(json.dumps(returnSpace))
    myAWSIoTMQTTClient.publish(SpaceTopic, json.dumps(returnSpace), 1)
    print("Updated Space successfully")


