import cv2
import numpy as np
import RPi.GPIO as gpio
from matplotlib.pyplot import text
import numpy as np
import Falcon
import imutils
import time

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

#-------#Setup Camera-------#
cap = cv2.VideoCapture(0)
cap.set(3, 160)
cap.set(4, 120)
cap.set(cv2.CAP_PROP_BRIGHTNESS, 52)
cap.set(cv2.CAP_PROP_SATURATION, 50)
cap.set(cv2.CAP_PROP_CONTRAST, 40)
#---------------------------#

#------------#LineDetection------------#
max_speed= 70
min_speed= 64

print("FALCON is ON,,")
Falcon.SpeakBegin()
Falcon.FrontLight()

while True:
    ret, frame = cap.read()
    low_b = np.uint8([5,5,5])
    high_b = np.uint8([0,0,0])
    mask = cv2.inRange(frame, high_b, low_b)
    contours, hierarchy = cv2.findContours(mask, 1, cv2.CHAIN_APPROX_NONE)
    if len(contours) > 0 :
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)
        if M["m00"] !=0 :
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            print("CX : "+str(cx)+"  CY : "+str(cy))
            if cx >= 120 :
                print("Turn Right")
                Falcon.TurnRight(min_speed,max_speed)            
            if cx < 120 and cx > 40 :
                print("On Track!")
                Falcon.Forward(min_speed)
            if cx <=40 :
                print("Turn Left")
                Falcon.TurnLeft(min_speed,max_speed)
            cv2.circle(frame, (cx,cy), 5, (255,255,255), -1)
    else :
        print("I don't see the line")
        Falcon.Stop()
    cv2.drawContours(frame, c, -1, (0,255,0), 1)
    cv2.imshow("Mask",mask)
    cv2.imshow("Frame",frame)
    if cv2.waitKey(1) & 0xff == ord('q'):   # 1 is the time in ms
        Falcon.Stop()
        break
cap.release()
cv2.destroyAllWindows()
