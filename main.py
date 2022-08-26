from colorDetection.colorprint import scanColor
from using_cv_demo1 import line_follow
from crossing import distance
from cameraInput import camera

from threading import Thread
from time import sleep 

import numpy as np
from matplotlib.pyplot import text
import numpy as np
import Falcon
import imutils
import RPi.GPIO as gpio
gpio.setmode(gpio.BCM)

#init threads
cameraThread = camera()
colorThread = scanColor()
lineThread = line_follow()
distanceThread = distance()

#-------#Setup Pinouts-------#
en1=20
en2=21
in1=17
in2=22
in3=23
in4=24
gpio.setmode(gpio.BCM)
gpio.setup(in1, gpio.OUT)
gpio.setup(in2, gpio.OUT)
gpio.setup(in3, gpio.OUT)
gpio.setup(in4, gpio.OUT)
gpio.setup(en1,gpio.OUT)
gpio.setup(en2,gpio.OUT)
#p1 = gpio.PWM(en1, 100)
#p2 = gpio.PWM(en2, 100)
Falcon.Stop()
#----------------------------#

colour = None
#ig we will have this function control the car
def maiin():
    color = colorThread.color
    dist = distanceThread.dist
    no_line = lineThread.no_line
    cx = lineThread.cx

    if dist < 5:
        Falcon.Stop()

    if colour == 'R' or colour == 'G':
        Falcon.Stop()
        sleep(5000)
        line_follow()

    if colour == 'B':
        Falcon.Stop()
        sleep(2000)
        line_follow()

    if no_line != True:
        if cx >= 120:
            print("Turn Right")
            Falcon.TurnRight(min_speed,max_speed)
        if cx < 120 and cx > 50:
            print("On Track!")
            Falcon.Forward(max_speed)
        if cx <= 50:
            print("Turn Left")
            Falcon.TurnLeft(min_speed,max_speed)

    else:
        Falcon.Forward(max_speed)
        sleep(1000)#enough time for line cut 15cm dist
        line_follow()



    #print(f"distance={dist}")
    #print(f"color={colorThread.color}")
    #print(cameraThread.frame)
    #print(f"frame={cameraThread.frame}")
    #print(f"line={line}")
#------------#Main------------#
max_speed= 70
min_speed= 64

print("FALCON is ON,,")
Falcon.SpeakBegin()
#Falcon.FrontLight()####################################################################################

if __name__ == '__main__':
    cameraThread.start()
    print("here we go")
    colorThread.frame = cameraThread.frame 
    lineThread.frame = cameraThread.frame
    distanceThread.start()
    colorThread.start()
    lineThread.start()

    while (True):
        maiin()
        colorThread.frame = cameraThread.frame 
        lineThread.frame = cameraThread.frame
        dist = distanceThread.dist
        sleep(2)

"""
for when task is done

colorThread.stop()
lineThread.stop()
distanceThread.stop()
cameraThread.stop()

"""
